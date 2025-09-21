from typing import List, Dict, Any, Optional
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain.schema import Document
import os

from src.utils.config import config
from src.utils.logger import log_error
from src.models.document import Document as DocModel


class VectorStoreService:
    def __init__(self):
        # Initialize embeddings
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=config.EMBEDDING_MODEL, google_api_key=config.GOOGLE_API_KEY
        )

        # Ensure Chroma directory exists
        os.makedirs(config.CHROMA_PERSIST_DIR, exist_ok=True)

        # Initialize Chroma vector store
        self.vector_store = Chroma(
            persist_directory=config.CHROMA_PERSIST_DIR,
            embedding_function=self.embeddings,
            collection_name="lega_documents",
        )

    def add_document(
        self, document_id: str, text: str, metadata: Dict[str, Any] = None
    ) -> bool:
        """Add a document to the vector store."""
        try:
            # Create document chunks for better retrieval
            chunks = self._chunk_document(text)

            documents = []
            metadatas = []
            ids = []

            for i, chunk in enumerate(chunks):
                chunk_metadata = {
                    "document_id": document_id,
                    "chunk_id": i,
                    "chunk_type": "text",
                    **(metadata or {}),
                }

                documents.append(chunk)
                metadatas.append(chunk_metadata)
                ids.append(f"{document_id}_chunk_{i}")

            # Add to vector store
            self.vector_store.add_texts(texts=documents, metadatas=metadatas, ids=ids)

            return True

        except Exception as e:
            log_error(f"Error adding document to vector store: {str(e)}")
            return False

    def search_similar_documents(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents based on query."""
        try:
            results = self.vector_store.similarity_search_with_score(query=query, k=k)

            formatted_results = []
            for doc, score in results:
                formatted_results.append(
                    {
                        "content": doc.page_content,
                        "metadata": doc.metadata,
                        "similarity_score": score,
                    }
                )

            return formatted_results

        except Exception as e:
            log_error(f"Error searching vector store: {str(e)}")
            return []

    def search_document_clauses(
        self, document_id: str, query: str, k: int = 3
    ) -> List[Dict[str, Any]]:
        """Search for specific clauses within a document."""
        try:
            # Filter by document_id
            results = self.vector_store.similarity_search_with_score(
                query=query, k=k, filter={"document_id": document_id}
            )

            formatted_results = []
            for doc, score in results:
                formatted_results.append(
                    {
                        "content": doc.page_content,
                        "metadata": doc.metadata,
                        "similarity_score": score,
                    }
                )

            return formatted_results

        except Exception as e:
            log_error(f"Error searching document clauses: {str(e)}")
            return []

    def get_document_context(
        self, document_id: str, query: str, max_chunks: int = 5
    ) -> str:
        """Get relevant context from a document for Q&A."""
        try:
            results = self.search_document_clauses(document_id, query, k=max_chunks)

            # Combine relevant chunks
            context_parts = []
            for result in results:
                if result["similarity_score"] < 0.8:  # Only use highly relevant chunks
                    context_parts.append(result["content"])

            return "\n\n".join(context_parts)

        except Exception as e:
            log_error(f"Error getting document context: {str(e)}")
            return ""

    def remove_document(self, document_id: str) -> bool:
        """Remove a document and all its chunks from the vector store."""
        try:
            # Get all chunks for this document
            results = self.vector_store.get(where={"document_id": document_id})

            if results and results.get("ids"):
                # Delete all chunks
                self.vector_store.delete(ids=results["ids"])

            return True

        except Exception as e:
            log_error(f"Error removing document from vector store: {str(e)}")
            return False

    def get_document_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store."""
        try:
            # Get collection info
            collection = self.vector_store._collection
            count = collection.count()

            return {
                "total_documents": count,
                "collection_name": "lega_documents",
                "persist_directory": config.CHROMA_PERSIST_DIR,
            }

        except Exception as e:
            log_error(f"Error getting vector store stats: {str(e)}")
            return {"total_documents": 0}

    def _chunk_document(
        self, text: str, chunk_size: int = 1000, overlap: int = 200
    ) -> List[str]:
        """Split document into chunks for embedding."""
        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]

            # Try to break at sentence boundary
            if end < len(text):
                last_period = chunk.rfind(".")
                if last_period > chunk_size // 2:
                    chunk = chunk[: last_period + 1]
                    end = start + last_period + 1

            chunks.append(chunk.strip())
            start = end - overlap

        return [chunk for chunk in chunks if chunk.strip()]

    def find_similar_clauses(
        self, clause_text: str, exclude_document_id: str = None, k: int = 3
    ) -> List[Dict[str, Any]]:
        """Find similar clauses across all documents."""
        try:
            filter_dict = {}
            if exclude_document_id:
                # This is a simplified filter - Chroma might need different syntax
                filter_dict = {"document_id": {"$ne": exclude_document_id}}

            results = self.vector_store.similarity_search_with_score(
                query=clause_text, k=k, filter=filter_dict if filter_dict else None
            )

            formatted_results = []
            for doc, score in results:
                formatted_results.append(
                    {
                        "content": doc.page_content,
                        "metadata": doc.metadata,
                        "similarity_score": score,
                    }
                )

            return formatted_results

        except Exception as e:
            log_error(f"Error finding similar clauses: {str(e)}")
            return []
