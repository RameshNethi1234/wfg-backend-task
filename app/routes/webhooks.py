from fastapi import APIRouter, Depends, BackgroundTasks, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import get_db
from app.models import Transaction
from app.schemas import TransactionWebhookPayload
from app.workers import process_transaction

router = APIRouter(prefix="/v1/webhooks", tags=["Webhooks"])


@router.post(
    "/transactions",
    status_code=status.HTTP_202_ACCEPTED
)
async def receive_transaction_webhook(
    payload: TransactionWebhookPayload,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    # ---- Idempotency check ----
    stmt = select(Transaction).where(
        Transaction.transaction_id == payload.transaction_id
    )
    existing_txn = db.execute(stmt).scalar_one_or_none()

    if existing_txn:
        # Already received → do nothing
        return {"message": "Transaction already received"}

    # ---- Insert new transaction ----
    txn = Transaction(
        transaction_id=payload.transaction_id,
        source_account=payload.source_account,
        destination_account=payload.destination_account,
        amount=payload.amount,
        currency=payload.currency,
        status="PROCESSING",
    )

    db.add(txn)
    db.commit()

    # ---- Trigger background processing ----
    background_tasks.add_task(
        process_transaction,
        payload.transaction_id,
        db,
    )

    return {"message": "Transaction accepted for processing"}
