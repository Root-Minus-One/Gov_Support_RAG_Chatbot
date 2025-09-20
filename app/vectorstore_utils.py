from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from typing import List


def create_faiss_index(text: List[str]):
    embeddings = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-mpnet-base-v2")
    return FAISS.from_texts(text, embeddings)


def retrieve_docs(vectorstore: FAISS, query: str, k: int = 4):
    return vectorstore.similarity_search(query, k = k)