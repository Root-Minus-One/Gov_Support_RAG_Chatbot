from langchain_huggingface import HuggingFaceEmbeddings 


def HGF_embedder(model: str= "sentence-transformers/all-MiniLM-L6-v2"):
    embedding_model = HuggingFaceEmbeddings(model_name= model)

    return embedding_model


# src/embeddings/embedder.py
from .embedding_model import load_embedding_model, batch_encode

class Embedder:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = load_embedding_model(model_name)

    def encode(self, texts):
        return batch_encode(self.model, texts)
