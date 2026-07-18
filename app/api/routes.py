# routes.py
from pydantic import BaseModel
from fastapi import APIRouter, BackgroundTasks
from typing import Optional
from pathlib import Path

from app.core.config import settings
from app.rag.ingest import ingest_folder
from app.db.postgres import get_pool
from app.core.config import settings
from app.rag.embeddings import run_embedding_pipeline
from app.rag.generation import generate_answer
from app.rag.retrieval import retrieve_chunks
from app.middleware.rate_limiter import limiter

#import extractor # still need this for the extraction function call


router = APIRouter()


# @router.get("/")
# def home():
#     return render_template("chat.html")


@router.post("/ingest")
async def ingest_pdfs(background_tasks: BackgroundTasks, folder_path: Optional[str]=None):
    _f_path = Path(folder_path) if folder_path else Path(settings.DATA_ROOT_DIR)
    background_tasks.add_task(ingest_folder, _f_path)
    
    return {"message": "Ingestion started"}


@router.get("/ingest/status")
async def ingest_status(limit: int = 20):
    pool = get_pool()
    query = f"SELECT * FROM ingestion_log ORDER BY logged_at DESC LIMIT $1"

    async with pool.acquire() as conn:
        rows = await conn.fetch(query, limit)
    return [dict(row) for row in rows]



@router.post("/embed")
async def run_embeddings(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_embedding_pipeline)
    return {"message": "Embedding pipeline started"}



class ChatRequest(BaseModel):
    question : str
    category : str | None = None

@router.post("/chat")
@limiter.limit("5/minute")
async def chat(request: ChatRequest):
    chunks = await retrieve_chunks(question=request.question, category=request.category)

    if not chunks:
        return {"question": request.question, "answer": "I don't have information on this topic.", "sources": []}

    answer = generate_answer(request.question, chunks)
    
    sources = [{"doc_id": c["doc_id"], "category": c["category"], "score": c["score"]} for c in chunks]

    return {"question": request.question, "answer": answer, "source": sources}


# @router.get("/msg")
# def chat():
#     msg= request.form["msg"]
#     input= msg
#     print(input)
#     response = rag_chain.invoke({"input" : msg})
#     print("Response : ", response["answer"])
#     return str(response["answer"])



# if __name__ == '__main__':
#     app.run(host = "0.0.0.0", port = 8080, debug = True)