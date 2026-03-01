"""配置模块"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# 项目路径
BASE_DIR = Path(__file__).parent.parent
PROJECT_ROOT = BASE_DIR.parent

# 知识库路径（优先使用 qa_web 内的副本，便于部署）
_kb_in_app = BASE_DIR / "knowledge_base"
_kb_in_root = PROJECT_ROOT / "knowledge_base"
KNOWLEDGE_BASE_DIR = _kb_in_app if _kb_in_app.exists() else _kb_in_root

# 数据库 - 优先使用 Railway Volume 路径
VOLUME_DATA_PATH = Path("/app/data")
if VOLUME_DATA_PATH.exists():
    DATABASE_PATH = VOLUME_DATA_PATH / "qa.db"
else:
    DATABASE_PATH = BASE_DIR / "data" / "qa.db"  # 本地开发

# AI API 配置
API_KEY = os.getenv("API_KEY", "")
ANTHROPIC_BASE_URL = os.getenv("ANTHROPIC_BASE_URL", "https://api.ppinfra.com/anthropic")
AI_MODEL = os.getenv("AI_MODEL", "claude-sonnet-4-5-20250929")

# 服务器配置
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8080"))
