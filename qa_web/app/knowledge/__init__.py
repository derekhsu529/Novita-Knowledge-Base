"""知识库搜索和问答模块"""

from .search import search_knowledge_base
from .qa_engine import generate_answer

__all__ = ['search_knowledge_base', 'generate_answer']
