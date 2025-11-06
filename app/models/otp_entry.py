# app/models/otp_entry.py
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timedelta, timezone
import uuid
from app.db.base import Base

class OtpEntry(Base):
    __tablename__ = "otp_entries"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone = Column(String, nullable=True, index=True)  # For SMS OTP
    email = Column(String, nullable=True, index=True)  # For Email OTP
    code = Column(String, nullable=False)
    expires_at = Column(DateTime, default=lambda: datetime.now(timezone.utc) + timedelta(minutes=10))
