# main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes import router
#import extractor

### Main.py is the app and the routes are in routes.py and when api call happens it goes to routes.py from 


# 1. The Lifespan Manager (The New Way)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP: Load the heavy models once ---
    print("Initializing Docling Engine... Please wait.")
    app.state.converter = extractor.get_docling_converter()
    print("Docling Engine Loaded and Ready!")
    
    yield  # The app runs while it 'yields' here
    
    # --- SHUTDOWN: Clean up if necessary ---
    print("Shutting down... Cleaning up resources.")

# 2. Initialize FastAPI with the lifespan
app = FastAPI(lifespan=lifespan)

# 3. Include your routes
app.include_router(router)
