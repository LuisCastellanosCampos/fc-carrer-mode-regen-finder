"""
Entry point for the application.
Run with: uvicorn main:app --reload (from BACKEND/ directory)
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
