def get_prompt_template(question: str, chunks: list[dict]) -> str:
    context = "\n\n".join([chunk["chunk_text"] for chunk in chunks])
    
    return f"""You are a helpful assistant for AP government MSME schemes.
Use ONLY the provided context to answer the question.
If the answer is not in the context, say "I don't have information on this."
Keep your answer concise and accurate.

Context:
{context}

Question:
{question}

Answer:"""