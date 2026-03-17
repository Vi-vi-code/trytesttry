from fastapi import FastAPI
from app.routes import chat, drinking_logs, auth

#宣告並建立 FastAPI 伺服器實體
app = FastAPI(
    title="Groq + Supabase Experiment",
    description="FastAPI backend for testing LLM with database context",
    version="0.1.0"
)

# Include routers (main-> chat -> supabase -> chat -> groq)
app.include_router(chat.router)
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(drinking_logs.router, prefix="/logs", tags=["drinking_logs"])

# 這邊api放到render上後才須注意
@app.get("/health")
async def health_check():
    """Basic health check endpoint."""
    return {"status": "healthy"}
