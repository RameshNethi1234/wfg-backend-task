from sqlalchemy import Column, String, Numeric, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(String, primary_key=True, index=True)
    source_account = Column(String, nullable=False)
    destination_account = Column(String, nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), nullable=False)

    status = Column(String, nullable=False, default="PROCESSING")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)
