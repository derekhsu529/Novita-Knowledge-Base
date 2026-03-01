"""Pydantic 数据模型"""

from typing import List, Optional
from pydantic import BaseModel


# 请求模型
class AskRequest(BaseModel):
    question: str
    image: Optional[str] = None  # base64 编码的图片


class FeedbackRequest(BaseModel):
    qa_id: int
    is_helpful: bool
    feedback_text: Optional[str] = None


# 响应模型
class MatchedDoc(BaseModel):
    title: str
    url: str
    score: int


class AskResponse(BaseModel):
    id: int
    question: str
    answer: str
    matched_docs: List[MatchedDoc]
    response_time_ms: int
    created_at: str


class FeedbackResponse(BaseModel):
    id: int
    qa_id: int
    is_helpful: bool
    created_at: str


class QARecord(BaseModel):
    id: int
    question: str
    answer: str
    matched_docs: Optional[str]
    response_time_ms: Optional[int]
    created_at: str
    feedback: Optional[bool]
    feedback_text: Optional[str] = None


class StatsOverview(BaseModel):
    total_questions: int
    total_feedback: int
    helpful_count: int
    not_helpful_count: int
    helpful_rate: float
    avg_response_time_ms: int


class DailyStat(BaseModel):
    date: str
    questions: int
    helpful: int
    not_helpful: int


class HotQuestion(BaseModel):
    question: str
    count: int
    last_asked: str
