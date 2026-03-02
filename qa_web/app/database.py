"""数据库操作模块"""

import json
import aiosqlite
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from .config import DATABASE_PATH


async def init_db():
    """初始化数据库表"""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    async with aiosqlite.connect(DATABASE_PATH) as db:
        # 问答记录表
        await db.execute("""
            CREATE TABLE IF NOT EXISTS qa_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                matched_docs TEXT,
                response_time_ms INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 用户评价表
        await db.execute("""
            CREATE TABLE IF NOT EXISTS feedbacks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                qa_id INTEGER NOT NULL,
                is_helpful BOOLEAN NOT NULL,
                feedback_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (qa_id) REFERENCES qa_records(id)
            )
        """)

        # 手工知识库表
        await db.execute("""
            CREATE TABLE IF NOT EXISTS manual_kb (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 创建索引
        await db.execute("CREATE INDEX IF NOT EXISTS idx_qa_created_at ON qa_records(created_at)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_feedbacks_qa_id ON feedbacks(qa_id)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_manual_kb_category ON manual_kb(category)")

        await db.commit()

        # 如果手工知识库为空，自动导入默认 FAQ 数据
        cursor = await db.execute("SELECT COUNT(*) FROM manual_kb")
        count = (await cursor.fetchone())[0]
        if count == 0:
            await _seed_manual_kb(db)


async def _seed_manual_kb(db):
    """自动填充默认 FAQ 数据（仅在表为空时调用）"""
    from .import_faq import FAQ_DATA
    for faq in FAQ_DATA:
        await db.execute(
            "INSERT INTO manual_kb (category, question, answer) VALUES (?, ?, ?)",
            (faq["category"], faq["question"], faq["answer"])
        )
    await db.commit()
    print(f"自动导入 {len(FAQ_DATA)} 条 FAQ 到手工知识库")


async def save_qa_record(question: str, answer: str, matched_docs: List[Dict],
                         response_time_ms: int) -> int:
    """保存问答记录，返回记录 ID"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            """INSERT INTO qa_records (question, answer, matched_docs, response_time_ms)
               VALUES (?, ?, ?, ?)""",
            (question, answer, json.dumps(matched_docs, ensure_ascii=False), response_time_ms)
        )
        await db.commit()
        return cursor.lastrowid


async def save_feedback(qa_id: int, is_helpful: bool, feedback_text: Optional[str] = None) -> int:
    """保存用户评价，返回评价 ID"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            "INSERT INTO feedbacks (qa_id, is_helpful, feedback_text) VALUES (?, ?, ?)",
            (qa_id, is_helpful, feedback_text)
        )
        await db.commit()
        return cursor.lastrowid


async def delete_qa_record(qa_id: int) -> bool:
    """删除问答记录及其关联的评价"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # 先删除关联的评价
        await db.execute("DELETE FROM feedbacks WHERE qa_id = ?", (qa_id,))
        # 再删除问答记录
        cursor = await db.execute("DELETE FROM qa_records WHERE id = ?", (qa_id,))
        await db.commit()
        return cursor.rowcount > 0


async def get_qa_history(limit: int = 20, offset: int = 0) -> List[Dict]:
    """获取问答历史记录"""
    from datetime import datetime, timezone, timedelta

    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            """SELECT q.*,
                      (SELECT is_helpful FROM feedbacks WHERE qa_id = q.id ORDER BY id DESC LIMIT 1) as feedback,
                      (SELECT feedback_text FROM feedbacks WHERE qa_id = q.id ORDER BY id DESC LIMIT 1) as feedback_text
               FROM qa_records q
               ORDER BY q.created_at DESC
               LIMIT ? OFFSET ?""",
            (limit, offset)
        )
        rows = await cursor.fetchall()

        # 转换时间为北京时间
        beijing_tz = timezone(timedelta(hours=8))
        result = []
        for row in rows:
            record = dict(row)
            if record.get('created_at'):
                try:
                    # 解析 UTC 时间字符串
                    utc_time = datetime.strptime(record['created_at'], "%Y-%m-%d %H:%M:%S")
                    utc_time = utc_time.replace(tzinfo=timezone.utc)
                    # 转换为北京时间
                    beijing_time = utc_time.astimezone(beijing_tz)
                    record['created_at'] = beijing_time.strftime("%Y-%m-%d %H:%M:%S")
                except Exception:
                    # 如果转换失败，保留原始时间
                    pass
            result.append(record)

        return result


async def get_stats_overview() -> Dict:
    """获取总体统计"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM qa_records")
        total_questions = (await cursor.fetchone())[0]

        cursor = await db.execute("SELECT COUNT(*) FROM feedbacks")
        total_feedback = (await cursor.fetchone())[0]

        cursor = await db.execute("SELECT COUNT(*) FROM feedbacks WHERE is_helpful = 1")
        helpful_count = (await cursor.fetchone())[0]

        not_helpful_count = total_feedback - helpful_count
        helpful_rate = (helpful_count / total_feedback * 100) if total_feedback > 0 else 0

        cursor = await db.execute("SELECT AVG(response_time_ms) FROM qa_records")
        avg_response_time = (await cursor.fetchone())[0] or 0

        return {
            "total_questions": total_questions,
            "total_feedback": total_feedback,
            "helpful_count": helpful_count,
            "not_helpful_count": not_helpful_count,
            "helpful_rate": round(helpful_rate, 1),
            "avg_response_time_ms": round(avg_response_time)
        }


async def get_daily_stats(days: int = 7) -> List[Dict]:
    """获取每日统计"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

        cursor = await db.execute("""
            SELECT
                DATE(q.created_at) as date,
                COUNT(q.id) as questions,
                SUM(CASE WHEN f.is_helpful = 1 THEN 1 ELSE 0 END) as helpful,
                SUM(CASE WHEN f.is_helpful = 0 THEN 1 ELSE 0 END) as not_helpful
            FROM qa_records q
            LEFT JOIN feedbacks f ON q.id = f.qa_id
            WHERE DATE(q.created_at) >= ?
            GROUP BY DATE(q.created_at)
            ORDER BY date DESC
        """, (start_date,))

        rows = await cursor.fetchall()
        return [{"date": row[0], "questions": row[1], "helpful": row[2] or 0, "not_helpful": row[3] or 0}
                for row in rows]


async def get_hot_questions(limit: int = 10) -> List[Dict]:
    """获取热门问题"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute("""
            SELECT question, COUNT(*) as count, MAX(created_at) as last_asked
            FROM qa_records
            GROUP BY question
            ORDER BY count DESC, last_asked DESC
            LIMIT ?
        """, (limit,))

        rows = await cursor.fetchall()
        return [{"question": row[0], "count": row[1], "last_asked": row[2]} for row in rows]


# ============ 手工知识库 CRUD ============

async def get_manual_kb_list(category: Optional[str] = None) -> List[Dict]:
    """获取手工知识库条目列表"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        if category:
            cursor = await db.execute(
                "SELECT * FROM manual_kb WHERE category = ? ORDER BY category, id",
                (category,)
            )
        else:
            cursor = await db.execute("SELECT * FROM manual_kb ORDER BY category, id")
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]


async def get_manual_kb_categories() -> List[str]:
    """获取所有分类"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            "SELECT DISTINCT category FROM manual_kb ORDER BY category"
        )
        rows = await cursor.fetchall()
        return [row[0] for row in rows]


async def create_manual_kb_entry(category: str, question: str, answer: str) -> int:
    """新增手工知识库条目，返回 ID"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            "INSERT INTO manual_kb (category, question, answer) VALUES (?, ?, ?)",
            (category, question, answer)
        )
        await db.commit()
        return cursor.lastrowid


async def update_manual_kb_entry(entry_id: int, category: str, question: str, answer: str) -> bool:
    """更新手工知识库条目"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            "UPDATE manual_kb SET category = ?, question = ?, answer = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (category, question, answer, entry_id)
        )
        await db.commit()
        return cursor.rowcount > 0


async def delete_manual_kb_entry(entry_id: int) -> bool:
    """删除手工知识库条目"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute("DELETE FROM manual_kb WHERE id = ?", (entry_id,))
        await db.commit()
        return cursor.rowcount > 0


async def search_manual_kb(keywords: set) -> List[Dict]:
    """搜索手工知识库，返回匹配的条目"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM manual_kb")
        rows = await cursor.fetchall()

        results = []
        for row in rows:
            row_dict = dict(row)
            q_lower = row_dict["question"].lower()
            a_lower = row_dict["answer"].lower()
            cat_lower = row_dict["category"].lower()

            score = 0
            for kw in keywords:
                if kw in q_lower:
                    score += 5
                if kw in cat_lower:
                    score += 3
                score += min(a_lower.count(kw), 3)

            if score > 0:
                row_dict["score"] = score
                results.append(row_dict)

        results.sort(key=lambda x: x["score"], reverse=True)
        return results
