from langchain.prompts.chat import ChatPromptTemplate
from models.llm_factory import get_google_genai, get_google_genai_embedding
from pydantic import BaseModel, Field
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document
from typing import List

class InfoFetcherAgent:
    def __init__(self):
        self.embed_model = get_google_genai_embedding()
        self.vector_store = InMemoryVectorStore(self.embed_model)

    def add_documents(self, docs: List[Document]):
       
        self.vector_store.add_documents(docs)

    def retrieve(self, query: str, top_k: int = 1) -> List[Document]:
      
        results = self.vector_store.similarity_search(query, top_k=top_k)
        return results

