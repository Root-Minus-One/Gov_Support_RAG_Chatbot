def main():
    print("Hello from gov-support-rag-chatbot!")

"""The main.py (The Entry Point)
This file is the "brain" of your application. You need it to:
Initialize the App: Create the FastAPI or Flask instance.
Register Routes: Import and include your routes.py using app.include_router.
Lifespan Events: Handle startup and shutdown tasks, such as connecting to your Vector Database or checking LLM API keys. 
"""


"""from fastapi import FastAPI
from contextlib import asynccontextmanager
from .routes import router as rag_router
# from .database import vector_db_client  # Hypothetical database connection

@asynccontextmanager
async def lifespan(app: FastAPI):
    "
    Handles startup and shutdown logic.
    Ideal for connecting/disconnecting from the Vector Database.
    "
    # STARTUP: Logic to run when the app starts
    print("🚀 Initializing RAG Pipeline and Vector DB connection...")
    # await vector_db_client.connect() 
    
    yield  # The app runs here
    
    # SHUTDOWN: Logic to run when the app stops
    print(" Closing connections...")
    # await vector_db_client.close()

# Create the FastAPI instance
app = FastAPI(
    title="Product Team RAG API",
    description="Internal RAG system with data managed by the product team.",
    version="1.0.0",
    lifespan=lifespan
)

# Include the routes from routes.py
# This connects your API endpoints to the main app instance
app.include_router(rag_router, prefix="/api/v1", tags=["RAG Operations"])

@app.get("/")
async def root():
    "Simple root endpoint for health checks."
    return {"message": "RAG API is live and healthy"}

if __name__ == "__main__":
    import uvicorn
    # Start the server locally on port 8000
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
"""

if __name__ == "__main__":
    main()
