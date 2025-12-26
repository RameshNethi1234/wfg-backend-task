from pydantic import BaseModel, Field
from decimal import Decimal

class TransactionWebhookPayload(BaseModel):
    transaction_id: str = Field(..., example="txn_123")
    source_account: str
    destination_account: str
    amount: Decimal
    currency: str


class TransactionStatusResponse(BaseModel):
    transaction_id: str
    status: str
    created_at: str
    processed_at: str | None
