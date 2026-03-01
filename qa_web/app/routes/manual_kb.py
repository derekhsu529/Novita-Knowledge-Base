"""手工知识库 API 路由"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from ..database import (
    get_manual_kb_list,
    get_manual_kb_categories,
    create_manual_kb_entry,
    update_manual_kb_entry,
    delete_manual_kb_entry,
)

router = APIRouter()


class ManualKBRequest(BaseModel):
    category: str
    question: str
    answer: str


@router.get("/list")
async def list_entries(category: Optional[str] = None):
    """获取手工知识库条目列表"""
    return await get_manual_kb_list(category)


@router.get("/categories")
async def list_categories():
    """获取所有分类"""
    return await get_manual_kb_categories()


@router.post("/create")
async def create_entry(req: ManualKBRequest):
    """新增条目"""
    entry_id = await create_manual_kb_entry(req.category, req.question, req.answer)
    return {"id": entry_id, "message": "创建成功"}


@router.put("/{entry_id}")
async def update_entry(entry_id: int, req: ManualKBRequest):
    """编辑条目"""
    success = await update_manual_kb_entry(entry_id, req.category, req.question, req.answer)
    if not success:
        raise HTTPException(status_code=404, detail="条目不存在")
    return {"message": "更新成功"}


@router.delete("/{entry_id}")
async def delete_entry(entry_id: int):
    """删除条目"""
    success = await delete_manual_kb_entry(entry_id)
    if not success:
        raise HTTPException(status_code=404, detail="条目不存在")
    return {"message": "删除成功"}
