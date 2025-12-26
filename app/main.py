from fastapi import FastAPI
from datetime import datetime

from app.config import APP_NAME, ENV
from app.database import engine
from app.models import Base
from app.routes.webhooks import router as webhook_router
from app.routes.transactions import router as transaction_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=APP_NAME,
    version="1.0.0",
    description="Webhook-based transaction processing service",
)

app.include_router(webhook_router)
app.include_router(transaction_router)


@app.get("/", tags=["Health"])
async def health_check():
    return {
        "status": "HEALTHY",
        "service": APP_NAME,
        "environment": ENV,
        "current_time": datetime.utcnow().isoformat(),
    }
