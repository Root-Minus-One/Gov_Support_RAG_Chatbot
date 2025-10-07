from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate




# src/generator/llm_interface.py
from langchain_huggingface import HuggingFaceEndpoint
import os

def get_llm(model_name="gemini-pro"):
    """
    Initialize the LLM interface using HuggingFace endpoint.
    """
    # huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY")

    os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY" 
    
    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.0) # temperature=0.0 for deterministic answers


    # llm = HuggingFaceEndpoint(model=model_name,
    #                           temperature=0.2,
    #                           max_new_tokens=512,
    #                           huggingfacehub_api_token=huggingface_api_key
    #                           )
    # return llm




import os
from dotenv import load_dotenv

# LangChain components
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

# Load environment variables (like GOOGLE_API_KEY)
load_dotenv()

# --- 1. Set up Google API Key ---
# LangChain will automatically look for GOOGLE_API_KEY environment variable.
# If not set, you can pass it directly:
# os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY"


# # For our dummy text file:
# from langchain_community.document_loaders import TextLoader
# loader = TextLoader("sample.txt")
# documents = loader.load()




# --- 5. Initialize the Gemini Chat Model ---
# ChatGoogleGenerativeAI is the class for Gemini chat models in LangChain
# model="gemini-pro" is the text-only Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.0) # temperature=0.0 for deterministic answers

print(f"Initialized Gemini model: {llm.model_name}")

# --- 6. Set up the QA Chain ---
# We'll use a standard QA chain for RAG
# Prompt template for better answer formatting
prompt_template = """
Answer the question based on the provided context only.
If the answer is not found in the context, politely state that you don't have enough information.

Context:
{context}

Question:
{question}

Answer:
"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

# Load the QA chain, specifying the Gemini LLM and prompt
chain = load_qa_chain(llm, chain_type="stuff", prompt=PROMPT) # 'stuff' combines all docs into one prompt

# --- 7. Perform QA ---
question = "What are large language models used for and what role does Gemini play?"
print(f"\n--- Asking Question ---")
print(f"Question: {question}")

# Retrieve relevant documents from the vector store
retrieved_docs = vector_store.similarity_search(question)
print(f"Retrieved {len(retrieved_docs)} relevant document(s).")

# Run the QA chain
try:
    response = chain.run(input_documents=retrieved_docs, question=question)
    print("\n--- Answer ---")
    print(response)
except Exception as e:
    print(f"An error occurred during QA: {e}")
    print("Please ensure your GOOGLE_API_KEY is correct and the Gemini model is accessible.")


# --- Another Question ---
question_2 = "What is the capital of France according to the document?"
print(f"\n--- Asking Another Question ---")
print(f"Question: {question_2}")

retrieved_docs_2 = vector_store.similarity_search(question_2)
print(f"Retrieved {len(retrieved_docs_2)} relevant document(s).")

try:
    response_2 = chain.run(input_documents=retrieved_docs_2, question=question_2)
    print("\n--- Answer ---")
    print(response_2)
except Exception as e:
    print(f"An error occurred during QA: {e}")