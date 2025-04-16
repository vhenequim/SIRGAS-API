from src.api import app

# This is a simple entry point for Render deployment
# It imports the FastAPI app from src/api.py

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 