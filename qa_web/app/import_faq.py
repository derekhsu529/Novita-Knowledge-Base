"""
FAQ 种子数据 - Novita AI
基于 novita-skills 知识库内容编写
"""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "data" / "qa.db"

FAQ_DATA = []


def import_faq():
    """导入FAQ数据到手工知识库"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(DB_PATH))

    conn.execute("""
        CREATE TABLE IF NOT EXISTS manual_kb (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_manual_kb_category ON manual_kb(category)")

    cursor = conn.execute("SELECT COUNT(*) FROM manual_kb")
    count = cursor.fetchone()[0]

    if count > 0:
        print(f"手工知识库已有 {count} 条数据。")
        choice = input("是否清空后重新导入？(y/N): ").strip().lower()
        if choice == 'y':
            conn.execute("DELETE FROM manual_kb")
            print("已清空旧数据。")
        else:
            print("取消导入。")
            conn.close()
            return

    for faq in FAQ_DATA:
        conn.execute(
            "INSERT INTO manual_kb (category, question, answer) VALUES (?, ?, ?)",
            (faq["category"], faq["question"], faq["answer"])
        )

    conn.commit()

    cursor = conn.execute("SELECT category, COUNT(*) FROM manual_kb GROUP BY category ORDER BY category")
    print(f"\n导入完成！共 {len(FAQ_DATA)} 条FAQ：")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]} 条")

    conn.close()


if __name__ == "__main__":
    import_faq()
