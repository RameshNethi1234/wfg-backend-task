from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import get_db
from app.models import Transaction
from app.schemas import TransactionStatusResponse

router = APIRouter(prefix="/v1/transactions", tags=["Transactions"])


@router.get("/{transaction_id}", response_model=TransactionStatusResponse)
async def get_transaction_status(
    transaction_id: str,
    db: Session = Depends(get_db),
):
    stmt = select(Transaction).where(
        Transaction.transaction_id == transaction_id
    )
    txn = db.execute(stmt).scalar_one_or_none()

    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return TransactionStatusResponse(
        transaction_id=txn.transaction_id,
        status=txn.status,
        created_at=txn.created_at.isoformat(),
        processed_at=txn.processed_at.isoformat() if txn.processed_at else None,
    )
