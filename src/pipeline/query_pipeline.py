from src.embeddings.embedder import HGF_embedder
from src.retriever.retriever import get_retriever
from src.generation.llm_interface import get_llm 
from src.generation.response_builder import generate_answer
import os







# Find documents
search_query = "Explain the constitution of India"

    # Perform the semantic search using the built-in vectorize
# search_results = collection.find(
#     sort={"$vectorize": search_query},
#     limit=3,
#     include_similarity=True
# )


def run_query():
    query = input("Ask your question: ")

    embeddings = HGF_embedder()
    
    retriever = get_retriever()

    llm = get_llm()
    result = generate_answer(query, retriever, llm)

    print("\nAnswer:\n", result["answer"])
    print("\nSources:\n", "\n".join(result["sources"]))

if __name__ == "__main__":
    run_query()
