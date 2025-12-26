import asyncio
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

from app.models import Transaction


async def process_transaction(transaction_id: str, db: Session):
    """
    Simulates a slow external API call (30s),
    then marks the transaction as PROCESSED.
    """
    await asyncio.sleep(30)

    stmt = select(Transaction).where(
        Transaction.transaction_id == transaction_id
    )
    txn = db.execute(stmt).scalar_one_or_none()

    if not txn:
        return

    txn.status = "PROCESSED"
    txn.processed_at = datetime.utcnow()

    db.commit()
