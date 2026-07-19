from langchain_community.retrievers import BM25Retriever
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever


from app.core.config import settings
from app.rag.embeddings import embed_texts


# 1. Embeddings wrapper

embeddings = HuggingFaceEmbeddings(model=settings.EMBEDDING_MODEL_NAME)

# 2. Pinecone vector store
class PineconeRetriever(BaseRetriever):
    top_k: int = 5

    def _get_relevant_documents(self, query: str) -> list[Document]:
        ...
    
     

)
# 3. BM25 retriever
# 4. Ensemble retriever
# 5. Prompt template
# 6. LLM
# 7. Chain
# 8. One function: async def rag_chain(question, category) -> dict