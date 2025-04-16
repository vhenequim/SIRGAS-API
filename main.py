from src.api import app

# This file is the entry point for Render deployment
# It imports the FastAPI app instance from src/api.py

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 