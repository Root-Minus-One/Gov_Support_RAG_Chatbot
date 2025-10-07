from flask import Flask, render_template, jsonify, request
from src.embeddings.embedder import HGF_embedder
from langchain_astradb import AstraDBVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.generation.prompts import *
import os



app = Flask(__name__)

load_dotenv()

ASTRA_DB_API_KEY = ""
GOOGLE_API_KEY = ""

os.environ["ASTRA_DB_API_KEY"] = ASTRA_DB_API_KEY
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY


embeddings = HGF_embedder()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.0)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}")
    ]
)


vstore = AstraDBVectorStore(
            collection_name= "DocStore",
            api_endpoint= ASTRA_DB_API_KEY,
            token="",
            embedding=HGF_embedder()
        ) 

db_retriever = vstore.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 3, "score_threshold": 0.1},
)


question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(db_retriever, question_answer_chain)

response = rag_chain.invoke({"input" : "What is Acticle 73 about in constitution of India?"})
print(response["answer"])



@app.route("/")
def home():
    return render_template("chat.html")


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg= request.form["msg"]
    input= msg
    print(input)
    response = rag_chain.invoke({"input" : msg})
    print("Response : ", response["answer"])
    return str(response["answer"])



if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 8080, debug = True)