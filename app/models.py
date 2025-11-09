from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

from app.database import Base


class Customer(Base):
    __tablename__ = 'customers'

    customer_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    kyc_status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)