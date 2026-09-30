# routes.py
from fastapi import Request, APIRouter, BackgroundTasks
from typing import Optional
from pathlib import Path

from app.db.postgres import get_pool

from app.core.config import settings

from app.rag.ingest import ingest_folder
from app.rag.embeddings import run_embedding_pipeline
from app.rag.gaurdrails import validate_input, check_relevance
from app.rag.pipeline import run_rag_pipeline
from app.middleware.rate_limiter import limiter

from app.schemas import ChatRequest, ChatResponse
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



@router.post("/chat", response_model=ChatResponse)
@limiter.limit("5/minute")
async def chat(request: Request, payload: ChatRequest):
    # Validate prompt
    is_valid, message = validate_input(payload.question)
    if not is_valid:
        return {"error": message}

    # Call pipeline with unpacked fields
    return await run_rag_pipeline(
        question = payload.question,
        session_id_input = getattr(payload, "session_id", None),
        category = getattr(payload, "category", None)
    )



# if __name__ == '__main__':
#     app.run(host = "0.0.0.0", port = 8080, debug = True)