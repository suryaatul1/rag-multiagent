import dataclasses
from typing import TypedDict, List

from langchain_classic.retrievers import EnsembleRetriever
from langchain_core.documents import Document


@dataclasses.dataclass
class AgentState(TypedDict):
    question: str
    documents: List[Document]
    draft_answer: str
    verification_report: str
    is_relevant: bool
    retriever: EnsembleRetriever
    relevance_model:str
    research_model:str
    verification_model:str