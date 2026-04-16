#from langchain_astradb import AstraDBVectorStore
from utils.config import get_api_key
from embeddings_manager import EmbeddingModel
from pinecone import Pinecone, ServerlessSpec
from typing import List
import dotenv

pc = Pinecone(api_key=get_api_key("PINECONE_API_KEY"))


"""
class VectorStoreManager:
__init__(self, embedding_model, vector_db_dir): Initializes with an embedding model and directory.

create_vector_store(self, chunks: list[dict], language: str) -> None: Takes chunks, computes embeddings, and builds a vector store for a given language.

initialize_vector_store(self, language: str): Loads an existing vector store for a specific language.

add_documents_to_store(self, new_chunks: list[dict], language: str) -> None: Adds new documents/chunks to an existing vector store.

get_retriever(self, language: str): Returns a retriever instance for a specific language's vector store (e.g., LangChain's VectorStoreRetriever).
"""

class VectorStoreManager:
    
    def __init__(self, config: dict):
        self.config = config
        self.vector_store_client = self._initialize_vector_store()
    
    # def _initialize_vector_store(self):
        
    #     collection = self.config.get("COLLECTION_NAME")
    #     api_key = get_api_key("ASTRADB_API_KEY")
    #     db_token = get_api_key("ASTRADB_TOKEN")
    #     embeddings = EmbeddingModel()

    #     if collection is None:
    #         raise ValueError(f"Collection name must be specified in")

    #     return AstraDBVectorStore(
    #         collection_name= collection,
    #         api_endpoint= api_key,
    #         token=db_token,
    #         embedding = embeddings.embedding_client
    #     )

    


    def pinecone_initialize(self, Index_name: str, vector_dimension: int, metric: str):
        """function to create pinecone index"""

        try:
            if not pc.has_index(Index_name):
                #_pinecone_key = os.getenv("PINECONE_API")
                #pc = Pinecone(_pinecone_key)

                pc.create_index(
                    name = Index_name,
                    dimension = vector_dimension,
                    metric = metric or "cosine",
                    spec = ServerlessSpec(
                    cloud  = "aws",
                    region = "us-east-1"
                ))

                print("success")
        except:
            pass


    def pinecone_upsert(self, Index_name: str, vector: List):
        """function to insert data into pinecone index"""
        try:
            index = pc.Index(Index_name)
            index.upsert(vectors=vector)

            print("done")

            return []
        
        except:
            pass


    def pinecone_query(self, Index_name: str, query_embedding, top_results: int):
        """function to query on pinecone index"""
        try:
            index = pc.Index(Index_name)
            pi_response = index.query(
                vector=query_embedding, #need to check query_embedding
                top_k = top_results,
                include_metadata=True
            )

            print("done")

            return []
        
        except:
            pass
