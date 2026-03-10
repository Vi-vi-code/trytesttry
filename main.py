from fastapi import FastAPI
from app.routes import chat

app = FastAPI(
    title="Groq + Supabase Experiment",
    description="FastAPI backend for testing LLM with database context",
    version="0.1.0"
)

# Include routers
app.include_router(chat.router)


@app.get("/health")
async def health_check():
    """Basic health check endpoint."""
    return {"status": "healthy"}
