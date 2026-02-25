import os.path
import sys

from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import Chroma

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from .embedding_model import EmbeddingModel
from project_root.my_configs.Setting import settings
from project_root.my_utilities.util_logging import logging

logger= logging.getLogger(__name__)



class RetrieverBuilder:
    def __init__(self):
        obj = EmbeddingModel()
        embedding_model = obj.get_embedding()
        self.embeddings = embedding_model

    def build_hybrid_retriever(self, docs):
        """Build a hybrid retriever using BM25 and vector-based retrieval."""
        try:
            # Create Chroma vector store
            vector_store = Chroma.from_documents(
                documents=docs,
                embedding=self.embeddings,
                persist_directory=settings.CHROMA_DB_PATH
            )
            logger.info("Vector store created successfully.")

            # Create BM25 retriever
            bm25 = BM25Retriever.from_documents(docs)
            logger.info("BM25 retriever created successfully.")

            # Create vector-based retriever
            vector_retriever = vector_store.as_retriever(search_kwargs={"k": settings.VECTOR_SEARCH_K})
            #vector_retriever = vector_store.as_retriever()
            logger.info("Vector retriever created successfully.")

            # Combine retrievers into a hybrid retriever
            hybrid_retriever = EnsembleRetriever(
                retrievers=[bm25, vector_retriever],
                weights=settings.HYBRID_RETRIEVER_WEIGHTS
            )
            logger.info("Hybrid retriever created successfully.")
            return hybrid_retriever
        except Exception as e:
            logger.error(f"Failed to build hybrid retriever: {e}")
            raise