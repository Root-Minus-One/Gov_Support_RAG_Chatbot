# src/generator/response.py
from langchain.chains import LLMChain
# from langchain.chains.combine_documents import StuffDocumentsChain
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.prompts import PromptTemplate




def generate_answer(query, retriever, llm):
    """
    Retrieve context from vector store and generate a response using the LLM.
    """
    # Create RAG chain
    rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",  # combine all docs into one prompt
        return_source_documents=True
    )

    result = rag_chain({"query": query})
    answer = result["result"]
    sources = [doc.metadata.get("source") for doc in result["source_documents"]]
    
    return {"answer": answer, "sources": sources}




