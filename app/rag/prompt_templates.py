from langchain.prompts import PromptTemplate


system_prompt = (
     """ You are an assistant for question-answering tasks.
     "Use the following places of retrieved content to answer the question.
     if you don't know the answer, say that you are not aware of that.
     Use three sentence maximum and keep the answer concise."""
     "\n\n"
     "{context}"
)


def create_prompt():
    """
    Create a custom RAG prompt template.
    """
    template = """
    You are a helpful AI assistant.
    Use the provided context to answer the question as accurately as possible.
    
    Context:
    {context}
    
    Question:
    {question}
    
    Answer:
    """
    return PromptTemplate(template=template, input_variables=["context", "question"])