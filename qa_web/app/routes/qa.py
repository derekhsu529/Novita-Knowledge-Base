"""问答 API 路由"""

import time
from typing import List
from fastapi import APIRouter, HTTPException
from ..models import AskRequest, AskResponse, FeedbackRequest, FeedbackResponse, QARecord, MatchedDoc
from ..database import save_qa_record, save_feedback, get_qa_history, delete_qa_record
from ..knowledge import search_knowledge_base, generate_answer
from ..knowledge.search import get_context_for_qa

router = APIRouter()


@router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    """提问并获得回答"""
    if not request.question.strip() and not request.image:
        raise HTTPException(status_code=400, detail="请输入问题或上传图片")

    start_time = time.time()

    try:
        # 1. 搜索知识库
        search_results = search_knowledge_base(request.question)

        # 2. 获取上下文
        context = get_context_for_qa(search_results)

        # 3. 生成回答（支持图片）
        answer = generate_answer(request.question, context, image_base64=request.image)

        # 4. 计算响应时间
        response_time_ms = int((time.time() - start_time) * 1000)

        # 5. 保存记录
        matched_docs = [
            {"title": r.title, "url": r.url, "score": r.score}
            for r in search_results
        ]
        qa_id = await save_qa_record(
            question=request.question,
            answer=answer,
            matched_docs=matched_docs,
            response_time_ms=response_time_ms
        )

        # 6. 返回响应
        return AskResponse(
            id=qa_id,
            question=request.question,
            answer=answer,
            matched_docs=[MatchedDoc(**doc) for doc in matched_docs],
            response_time_ms=response_time_ms,
            created_at=time.strftime("%Y-%m-%d %H:%M:%S")
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理问题时发生错误: {str(e)}")


@router.get("/history", response_model=List[QARecord])
async def get_history(limit: int = 20, offset: int = 0):
    """获取问答历史"""
    records = await get_qa_history(limit=limit, offset=offset)
    return [QARecord(**record) for record in records]


@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(request: FeedbackRequest):
    """提交评价"""
    try:
        feedback_id = await save_feedback(
            qa_id=request.qa_id,
            is_helpful=request.is_helpful,
            feedback_text=request.feedback_text
        )

        return FeedbackResponse(
            id=feedback_id,
            qa_id=request.qa_id,
            is_helpful=request.is_helpful,
            created_at=time.strftime("%Y-%m-%d %H:%M:%S")
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存评价时发生错误: {str(e)}")


@router.delete("/record/{qa_id}")
async def delete_record(qa_id: int):
    """删除问答记录"""
    try:
        success = await delete_qa_record(qa_id)
        if not success:
            raise HTTPException(status_code=404, detail="记录不存在")
        return {"success": True, "message": "删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除失败: {str(e)}")
