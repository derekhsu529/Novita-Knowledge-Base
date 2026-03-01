"""统计 API 路由"""

from typing import List
from fastapi import APIRouter
from ..models import StatsOverview, DailyStat, HotQuestion
from ..database import get_stats_overview, get_daily_stats, get_hot_questions

router = APIRouter()


@router.get("/overview", response_model=StatsOverview)
async def stats_overview():
    """获取总体统计"""
    stats = await get_stats_overview()
    return StatsOverview(**stats)


@router.get("/daily", response_model=List[DailyStat])
async def stats_daily(days: int = 7):
    """获取每日统计"""
    stats = await get_daily_stats(days=days)
    return [DailyStat(**s) for s in stats]


@router.get("/hot_questions", response_model=List[HotQuestion])
async def hot_questions(limit: int = 10):
    """获取热门问题"""
    questions = await get_hot_questions(limit=limit)
    return [HotQuestion(**q) for q in questions]
