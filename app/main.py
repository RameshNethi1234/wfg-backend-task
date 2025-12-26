from fastapi import FastAPI
from datetime import datetime
from app.config import APP_NAME, ENV

app = FastAPI(
    title=APP_NAME,
    version="1.0.0",
    description="Webhook-based transaction processing service"
)


@app.get("/", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    Used by load balancers / monitoring systems.
    """
    return {
        "status": "HEALTHY",
        "service": APP_NAME,
        "environment": ENV,
        "current_time": datetime.utcnow().isoformat()
    }
