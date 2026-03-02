"""FastAPI 应用入口"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import logging

from .database import init_db
from .routes import qa_router, stats_router, manual_kb_router
from .knowledge.search import _load_index, _read_kb_file_cached
from .config import KNOWLEDGE_BASE_DIR

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent.parent


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 1. 初始化数据库
    logger.info("初始化数据库...")
    await init_db()
    logger.info("数据库初始化完成")

    # 2. 预加载知识库到缓存
    logger.info("预加载知识库...")
    try:
        index = _load_index()
        count = 0
        for page in index["pages"]:
            doc_path = KNOWLEDGE_BASE_DIR / page["path"]
            if doc_path.exists():
                _read_kb_file_cached(str(doc_path))
                count += 1
        logger.info(f"知识库预加载完成：{count} 个文件已缓存")
    except Exception as e:
        logger.error(f"知识库预加载失败: {e}")

    yield

    logger.info("应用关闭")


app = FastAPI(
    title="接口AI 知识库问答",
    description="基于 jiekou.ai 知识库的智能问答系统",
    version="1.0.0",
    lifespan=lifespan
)

# 静态文件（仅在目录存在时挂载）
static_dir = BASE_DIR / "frontend" / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# API 路由
app.include_router(qa_router, prefix="/api/qa", tags=["问答"])
app.include_router(stats_router, prefix="/api/stats", tags=["统计"])
app.include_router(manual_kb_router, prefix="/api/manual-kb", tags=["手工知识库"])


@app.get("/")
async def serve_index():
    """问答页面"""
    return FileResponse(BASE_DIR / "frontend" / "index.html")


@app.get("/stats")
async def serve_stats():
    """统计页面"""
    return FileResponse(BASE_DIR / "frontend" / "stats.html")


@app.get("/manual-kb")
async def serve_manual_kb():
    """手工知识库管理页面"""
    return FileResponse(BASE_DIR / "frontend" / "manual_kb.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
