# src/retriever/retriever.py
from langchain_astradb import AstraDBVectorStore
from astrapy import DataAPIClient


# src/retriever.py
from src.storage.vectorstore import VectorStoreManager

class Retriever:
    def __init__(self, config):
        self.vstore = VectorStoreManager(config)
        self.retriever = self.vstore.get_retriever(k=5)

    def retrieve(self, query):
        pass