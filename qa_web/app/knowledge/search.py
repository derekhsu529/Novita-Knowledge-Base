"""知识库搜索模块 - 基于 test_qa.py 提取"""

import json
import sqlite3
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
from functools import lru_cache
from ..config import (KNOWLEDGE_BASE_DIR, DATABASE_PATH,
                      TAVILY_API_KEY, TAVILY_ENABLED, TAVILY_MAX_RESULTS,
                      TAVILY_SEARCH_DEPTH, TAVILY_TIMEOUT)

# 条件导入 Tavily 客户端
if TAVILY_ENABLED:
    try:
        from tavily import TavilyClient
        _tavily_client = None
    except ImportError:
        TAVILY_ENABLED = False
        print("⚠️  tavily-python 未安装，Tavily 搜索已禁用")

# 同义词/相关词映射表
SYNONYMS = {
    "视频": ["video", "i2v", "t2v", "v2v", "kling", "vidu", "wan", "sora", "veo", "hailuo", "minimax"],
    "图片": ["image", "img", "picture", "t2i", "i2i", "flux", "stable", "midjourney", "dall"],
    "音频": ["audio", "speech", "tts", "voice", "elevenlabs", "fish"],
    "文本": ["text", "llm", "chat", "gpt", "claude", "gemini", "qwen", "llama"],
    "价格": ["price", "pricing", "cost", "费用", "收费"],
    "调用": ["api", "sdk", "接口", "使用", "集成"],
    "vscode": ["vs code", "ide", "编辑器", "claude code", "插件"],
    "模型": ["model", "models"],
}

# 缓存知识库索引
_index_cache = None


@dataclass
class SearchResult:
    """搜索结果"""
    title: str
    path: str
    url: str
    score: int
    content_preview: str


def _load_index() -> Dict:
    """加载知识库索引（带缓存）"""
    global _index_cache
    if _index_cache is None:
        index_file = KNOWLEDGE_BASE_DIR / "_index.json"
        with open(index_file, encoding='utf-8') as f:
            _index_cache = json.load(f)
    return _index_cache


@lru_cache(maxsize=360)
def _read_kb_file_cached(path: str) -> str:
    """读取知识库文件（带 LRU 缓存）"""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def _clear_kb_cache():
    """清除知识库缓存（用于重新加载）"""
    _read_kb_file_cached.cache_clear()


def _expand_keywords(query: str) -> set:
    """扩展关键词，添加同义词"""
    query_lower = query.lower()
    keywords = set(query_lower.split())

    expanded = set(keywords)
    for word in keywords:
        for key, synonyms in SYNONYMS.items():
            if word in key or key in word:
                expanded.update(synonyms)
            if word in synonyms:
                expanded.add(key)
                expanded.update(synonyms)

    return expanded


def _get_tavily_client() -> Optional['TavilyClient']:
    """获取 Tavily 客户端（单例模式）"""
    global _tavily_client
    if not TAVILY_ENABLED or not TAVILY_API_KEY:
        return None

    if _tavily_client is None:
        from tavily import TavilyClient
        _tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

    return _tavily_client


async def _search_tavily_async(query: str) -> List[SearchResult]:
    """使用 Tavily 搜索网络资源（异步版本，带容错）"""
    client = _get_tavily_client()
    if not client:
        return []

    try:
        # 使用 asyncio.to_thread 将同步调用转为异步
        import asyncio
        response = await asyncio.to_thread(
            client.search,
            query=query,
            search_depth=TAVILY_SEARCH_DEPTH,
            max_results=TAVILY_MAX_RESULTS
        )

        results = []
        keywords = _expand_keywords(query)

        for idx, item in enumerate(response.get('results', [])):
            # 计算基础分数
            score = 5  # Tavily 基础分

            # 位置加权
            if idx == 0:
                score += 2
            elif idx == 1:
                score += 1

            # 标题关键词匹配
            title_lower = item.get('title', '').lower()
            if any(kw in title_lower for kw in keywords):
                score += 3

            results.append(SearchResult(
                title=f"[Web] {item.get('title', 'Untitled')}",
                path=f"tavily:{idx}",
                url=item.get('url', ''),
                score=score,
                content_preview=item.get('content', '')[:500]
            ))

        return results

    except Exception as e:
        # 静默失败，不影响本地搜索
        print(f"⚠️  Tavily 搜索失败: {e}")
        return []


def _search_tavily(query: str) -> List[SearchResult]:
    """使用 Tavily 搜索网络资源（同步版本，保持向后兼容）"""
    client = _get_tavily_client()
    if not client:
        return []

    try:
        response = client.search(
            query=query,
            search_depth=TAVILY_SEARCH_DEPTH,
            max_results=TAVILY_MAX_RESULTS
        )

        results = []
        keywords = _expand_keywords(query)

        for idx, item in enumerate(response.get('results', [])):
            score = 5
            if idx == 0:
                score += 2
            elif idx == 1:
                score += 1

            title_lower = item.get('title', '').lower()
            if any(kw in title_lower for kw in keywords):
                score += 3

            results.append(SearchResult(
                title=f"[Web] {item.get('title', 'Untitled')}",
                path=f"tavily:{idx}",
                url=item.get('url', ''),
                score=score,
                content_preview=item.get('content', '')[:500]
            ))

        return results

    except Exception as e:
        print(f"⚠️  Tavily 搜索失败: {e}")
        return []


def _search_in_content(content: str, keywords: set) -> int:
    """在文档内容中搜索关键词，返回匹配分数"""
    content_lower = content.lower()
    score = 0
    for kw in keywords:
        count = min(content_lower.count(kw), 5)
        score += count
    return score


def search_knowledge_base(query: str, max_docs: int = 8) -> List[SearchResult]:
    """
    搜索知识库，返回最相关的文档列表

    Args:
        query: 用户查询
        max_docs: 返回的最大文档数

    Returns:
        SearchResult 列表
    """
    index = _load_index()
    keywords = _expand_keywords(query)

    scored_docs = []
    for page in index["pages"]:
        title = page.get("title", "").lower()
        path = page.get("path", "").lower()

        # 标题和路径匹配（权重高）
        title_score = sum(3 for kw in keywords if kw in title)
        path_score = sum(2 for kw in keywords if kw in path)

        # 内容匹配
        doc_path = KNOWLEDGE_BASE_DIR / page["path"]
        content_score = 0
        content_preview = ""

        if doc_path.exists():
            try:
                content = _read_kb_file_cached(str(doc_path))
                content_score = _search_in_content(content, keywords)
                # 提取预览（跳过 frontmatter）
                lines = content.split('\n')
                start = 0
                if lines[0].strip() == '---':
                    for i, line in enumerate(lines[1:], 1):
                        if line.strip() == '---':
                            start = i + 1
                            break
                content_preview = '\n'.join(lines[start:start+10])[:500]
            except Exception:
                pass

        total_score = title_score + path_score + content_score
        if total_score > 0:
            scored_docs.append((total_score, page, content_preview))

    # 按分数排序
    scored_docs.sort(key=lambda x: x[0], reverse=True)
    top_docs = scored_docs[:max_docs]

    # 如果没有匹配，返回默认文档
    if not top_docs:
        for page in index["pages"][:max_docs]:
            doc_path = KNOWLEDGE_BASE_DIR / page["path"]
            content_preview = ""
            if doc_path.exists():
                content = _read_kb_file_cached(str(doc_path))
                content_preview = content[:500]
            top_docs.append((0, page, content_preview))

    results = []
    for score, doc, preview in top_docs:
        title = doc.get("title", "").strip()
        # 如果标题为空或是 Untitled，从内容中提取标题
        if not title or title.lower() == "untitled":
            title = _extract_title_from_content(doc["path"], preview)
        results.append(SearchResult(
            title=title,
            path=doc["path"],
            url=doc.get("url", ""),
            score=score,
            content_preview=preview
        ))

    # 合并手工知识库搜索结果
    manual_results = _search_manual_kb(keywords)
    results.extend(manual_results)

    # 集成 Tavily 网络搜索（如果启用）
    if TAVILY_ENABLED:
        tavily_results = _search_tavily(query)
        results.extend(tavily_results)

    # 按分数重新排序，取 top max_docs
    results.sort(key=lambda x: x.score, reverse=True)
    return results[:max_docs]


async def search_knowledge_base_async(query: str, max_docs: int = 8) -> List[SearchResult]:
    """
    搜索知识库（异步并行版本）

    同时执行本地搜索和 Tavily 网络搜索（如果启用），提高响应速度

    Args:
        query: 用户查询
        max_docs: 返回的最大文档数

    Returns:
        SearchResult 列表
    """
    import asyncio

    # 本地搜索（包括爬虫知识库和手工知识库）
    # 由于已经使用了文件缓存，本地搜索很快，可以同步执行
    index = _load_index()
    keywords = _expand_keywords(query)

    scored_docs = []
    for page in index["pages"]:
        title = page.get("title", "").lower()
        path = page.get("path", "").lower()

        title_score = sum(3 for kw in keywords if kw in title)
        path_score = sum(2 for kw in keywords if kw in path)

        doc_path = KNOWLEDGE_BASE_DIR / page["path"]
        content_score = 0
        content_preview = ""

        if doc_path.exists():
            try:
                content = _read_kb_file_cached(str(doc_path))
                content_score = _search_in_content(content, keywords)
                lines = content.split('\n')
                start = 0
                if lines[0].strip() == '---':
                    for i, line in enumerate(lines[1:], 1):
                        if line.strip() == '---':
                            start = i + 1
                            break
                content_preview = '\n'.join(lines[start:start+10])[:500]
            except Exception:
                pass

        total_score = title_score + path_score + content_score
        if total_score > 0:
            scored_docs.append((total_score, page, content_preview))

    scored_docs.sort(key=lambda x: x[0], reverse=True)
    top_docs = scored_docs[:max_docs]

    if not top_docs:
        for page in index["pages"][:max_docs]:
            doc_path = KNOWLEDGE_BASE_DIR / page["path"]
            content_preview = ""
            if doc_path.exists():
                content = _read_kb_file_cached(str(doc_path))
                content_preview = content[:500]
            top_docs.append((0, page, content_preview))

    results = []
    for score, doc, preview in top_docs:
        title = doc.get("title", "").strip()
        if not title or title.lower() == "untitled":
            title = _extract_title_from_content(doc["path"], preview)
        results.append(SearchResult(
            title=title,
            path=doc["path"],
            url=doc.get("url", ""),
            score=score,
            content_preview=preview
        ))

    # 合并手工知识库
    manual_results = _search_manual_kb(keywords)
    results.extend(manual_results)

    # 如果启用 Tavily，并行搜索
    if TAVILY_ENABLED:
        tavily_results = await _search_tavily_async(query)
        results.extend(tavily_results)

    # 按分数重新排序
    results.sort(key=lambda x: x.score, reverse=True)
    return results[:max_docs]


def _extract_title_from_content(path: str, preview: str) -> str:
    """从文档内容中提取标题"""
    lines = preview.split('\n')

    # 先尝试找 # 开头的标题行，或 === 下划线标题
    for i, line in enumerate(lines):
        stripped = line.strip()
        # # 开头的标题
        if stripped.startswith('#'):
            title = stripped.lstrip('#').strip()
            if title:
                return title
        # 检查下一行是否是 === 或 ---（Markdown setext 标题格式）
        if i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            if next_line and (next_line.startswith('===') or next_line.startswith('---')):
                if stripped and not stripped.startswith('```'):
                    return stripped

    # 如果没找到标题，取第一行非空文本
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith('===') and not stripped.startswith('---') and not stripped.startswith('```'):
            return stripped[:60] + ('...' if len(stripped) > 60 else '')

    # 最后使用文件名
    filename = path.replace("\\", "/").split("/")[-1].rsplit(".", 1)[0]
    return filename.replace("_", " ").replace("-", " ").title()


def _search_manual_kb(keywords: set) -> List[SearchResult]:
    """搜索手工知识库（同步，用于与文件知识库合并）"""
    if not DATABASE_PATH.exists():
        return []

    results = []
    try:
        conn = sqlite3.connect(str(DATABASE_PATH))
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("SELECT * FROM manual_kb")
        rows = cursor.fetchall()
        conn.close()
    except Exception:
        return []

    for row in rows:
        q_lower = row["question"].lower()
        a_lower = row["answer"].lower()
        cat_lower = row["category"].lower()

        score = 0
        for kw in keywords:
            if kw in q_lower:
                score += 5
            if kw in cat_lower:
                score += 3
            score += min(a_lower.count(kw), 3)

        if score > 0:
            # 手工知识库额外加权
            results.append(SearchResult(
                title=f"[FAQ] {row['question']}",
                path=f"manual_kb:{row['id']}",
                url="",
                score=score + 10,  # 手工知识库优先
                content_preview=row["answer"][:500]
            ))

    results.sort(key=lambda x: x.score, reverse=True)
    return results


def get_context_for_qa(results: List[SearchResult]) -> str:
    """将搜索结果转换为问答上下文（支持 Tavily）"""
    contents = []
    for result in results:
        if result.path.startswith("manual_kb:"):
            # 手工知识库条目，内容已在 content_preview 中
            contents.append(f"### {result.title}\n{result.content_preview}")

        elif result.path.startswith("tavily:"):
            # Tavily 网络搜索结果
            contents.append(
                f"### {result.title}\n"
                f"Source: {result.url}\n"
                f"{result.content_preview}"
            )

        else:
            # 爬虫知识库
            doc_path = KNOWLEDGE_BASE_DIR / result.path
            if doc_path.exists():
                content = _read_kb_file_cached(str(doc_path))
                contents.append(f"### {result.title}\nURL: {result.url}\n{content[:3000]}")

    return "\n\n---\n\n".join(contents)
