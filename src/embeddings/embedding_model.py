# src/embeddings/embedding_model.py
from sentence_transformers import SentenceTransformer
import torch

def load_embedding_model(model_name):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    return SentenceTransformer(model_name, device=device)

def batch_encode(model, texts, batch_size=32):
    return model.encode(texts, batch_size=batch_size, show_progress_bar=True)