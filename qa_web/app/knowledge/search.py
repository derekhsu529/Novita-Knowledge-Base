"""知识库搜索模块"""

import json
import sqlite3
from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass
from ..config import KNOWLEDGE_BASE_DIR, DATABASE_PATH

# 同义词/相关词映射表（Novita AI 产品相关）
SYNONYMS = {
    "llm": ["chat", "completion", "gpt", "claude", "gemini", "qwen", "llama", "deepseek", "model", "语言模型"],
    "gpu": ["显卡", "算力", "instance", "serverless", "nvidia", "a100", "h100", "l40s"],
    "sandbox": ["沙箱", "agent", "代理", "环境", "container", "容器"],
    "api": ["接口", "调用", "sdk", "endpoint", "端点"],
    "价格": ["price", "pricing", "cost", "费用", "收费", "计费", "billing"],
    "集成": ["integration", "cursor", "continue", "langchain", "llamaindex", "framework"],
    "图片": ["image", "img", "picture", "generation", "flux", "stable diffusion"],
    "模型": ["model", "models"],
    "认证": ["auth", "authentication", "api key", "token", "密钥"],
    "错误": ["error", "issue", "problem", "bug", "fail", "故障", "报错"],
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


def _search_in_content(content: str, keywords: set) -> int:
    """在文档内容中搜索关键词，返回匹配分数"""
    content_lower = content.lower()
    score = 0
    for kw in keywords:
        count = min(content_lower.count(kw), 5)
        score += count
    return score


def search_knowledge_base(query: str, max_docs: int = 8) -> List[SearchResult]:
    """搜索知识库，返回最相关的文档列表"""
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
                with open(doc_path, encoding='utf-8') as f:
                    content = f.read()
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
                with open(doc_path, encoding='utf-8') as f:
                    content_preview = f.read()[:500]
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

    # 合并手工知识库搜索结果
    manual_results = _search_manual_kb(keywords)
    results.extend(manual_results)

    # 按分数重新排序，取 top max_docs
    results.sort(key=lambda x: x.score, reverse=True)
    return results[:max_docs]


def _extract_title_from_content(path: str, preview: str) -> str:
    """从文档内容中提取标题"""
    lines = preview.split('\n')

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('#'):
            title = stripped.lstrip('#').strip()
            if title:
                return title
        if i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            if next_line and (next_line.startswith('===') or next_line.startswith('---')):
                if stripped and not stripped.startswith('```'):
                    return stripped

    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith('===') and not stripped.startswith('---') and not stripped.startswith('```'):
            return stripped[:60] + ('...' if len(stripped) > 60 else '')

    filename = path.replace("\\", "/").split("/")[-1].rsplit(".", 1)[0]
    return filename.replace("_", " ").replace("-", " ").title()


# 中文分类 → 英文映射
CATEGORY_EN = {
    "账户与计费": "Account & Billing",
    "LLM API": "LLM API",
    "GPU实例": "GPU Instances",
    "图像/视频生成": "Image/Video Generation",
    "Serverless": "Serverless",
    "其他": "General",
}


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
            cat_en = CATEGORY_EN.get(row['category'], row['category'])
            results.append(SearchResult(
                title=f"[FAQ - {cat_en}] #{row['id']}",
                path=f"manual_kb:{row['id']}",
                url="",
                score=score + 10,  # 手工知识库优先
                content_preview=row["answer"][:500]
            ))

    results.sort(key=lambda x: x.score, reverse=True)
    return results


def get_context_for_qa(results: List[SearchResult]) -> str:
    """将搜索结果转换为问答上下文"""
    contents = []
    for result in results:
        if result.path.startswith("manual_kb:"):
            contents.append(f"### {result.title}\n{result.content_preview}")
        else:
            doc_path = KNOWLEDGE_BASE_DIR / result.path
            if doc_path.exists():
                with open(doc_path, encoding='utf-8') as f:
                    content = f.read()
                    contents.append(f"### {result.title}\nURL: {result.url}\n{content[:3000]}")

    return "\n\n---\n\n".join(contents)
