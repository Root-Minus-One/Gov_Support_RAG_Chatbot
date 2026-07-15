# routes.py
from fastapi import APIRouter, BackgroundTasks
from typing import Optional
from pathlib import Path

from app.core.config import settings
from app.rag.ingest import ingest_folder
from app.db.postgres import get_pool
from app.core.config import settings

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