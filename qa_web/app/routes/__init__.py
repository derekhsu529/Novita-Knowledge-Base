"""API 路由模块"""

from .qa import router as qa_router
from .stats import router as stats_router
from .manual_kb import router as manual_kb_router

__all__ = ['qa_router', 'stats_router', 'manual_kb_router']
