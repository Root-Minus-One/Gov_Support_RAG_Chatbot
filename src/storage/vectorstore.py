from langchain_astradb import AstraDBVectorStore
# src/vectorstore.py
from langchain.vectorstores import AstraDB
from src.embeddings.embedder import HGF_embedder 

class VectorStoreManager:
    def __init__(self, astra_config):
        self.embeddings = HGF_embedder()
        self.vstore = AstraDB(
            collection_name=astra_config["collection_name"],
            api_endpoint=astra_config["api_endpoint"],
            token=astra_config["token"],
            namespace=astra_config["namespace"],
            embedding=self.embeddings
        )

    
    # def create_vector_store(collection_name, embedding_model, token, api_endpoint):
        
    #     vstore = AstraDBVectorStore(
    #         collection_name="DocStore",
    #         embedding = embedding_model,
    #         token= token,
    #         api_endpoint= api_endpoint
    #         )
        
    #     return vstore

    def add_documents(self, docs):
        self.vstore.add_documents(docs)


    def get_retriever(self, k=5):
        return self.vstore.as_retriever(search_kwargs={"k": k})
    
    
    def similarity_search(self, collection, search_query, k=5):
        self.search_results = collection.find(
            sort={"$vectorize": search_query},
            limit=3,
            include_similarity=True
            )
        return self.search_results

    
    def delete_all(self):
        self.vstore.delete_collection()



