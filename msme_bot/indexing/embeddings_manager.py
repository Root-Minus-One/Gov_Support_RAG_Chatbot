from utils.config import load_config
from utils.config import get_api_key 

#from langchain_huggingface import HuggingFaceEmbeddings 
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

from typing import List, Any
from pydantic import SecretStr



class EmbeddingModel:
    """Manages the loading and usage of the embedding model."""
    
    def __init__(self):
        "Initializes the EmbeddingModel by loading the specified embedding model."

        self.configuration = load_config()
        self.model = self.configuration["embedding_model"]["model_name"]
        self.embedding_client = self._get_embedding_instance()
    
    
    def _get_embedding_instance(self):
        return GoogleGenerativeAIEmbeddings(model= self.model, 
                                            google_api_key= SecretStr(get_api_key("GOOGLE_API_KEY"))
                                            )
    
    def embed_doc(self, text):
        """Embeds a list of documents."""
        embed_model = self._get_embedding_instance()
        return embed_model.embed_documents(text)
    
    def embed_query(self, query):
        """Embeds a query string"""

        embed_model = self._get_embedding_instance()
        return embed_model.embed_query(query)

    # def HGF_embedder(model: str = "sentence-transformers/all-MiniLM-L6-v2"):
    #     embedding_model = HuggingFaceEmbeddings(model_name= load_config)

    #     return embedding_model