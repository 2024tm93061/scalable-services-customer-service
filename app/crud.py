from sqlalchemy.orm import Session
from app import models
from typing import Dict, Any, List, Optional


def create_customer(db: Session, customer_data: Dict[str, Any]) -> models.Customer:
    db_customer = models.Customer(**customer_data)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def get_customer(db: Session, customer_id: int) -> Optional[models.Customer]:
    return db.query(models.Customer).filter(models.Customer.customer_id == customer_id).first()


def get_customers(db: Session, skip: int = 0, limit: int = 100) -> List[models.Customer]:
    return db.query(models.Customer).offset(skip).limit(limit).all()


def update_customer(db: Session, customer_id: int, updates: Dict[str, Any]) -> Optional[models.Customer]:
    customer = db.query(models.Customer).filter(models.Customer.customer_id == customer_id).first()
    if customer:
        for k, v in updates.items():
            if hasattr(customer, k) and v is not None:
                setattr(customer, k, v)
        db.commit()
        db.refresh(customer)
    return customer


def delete_customer(db: Session, customer_id: int) -> bool:
    customer = db.query(models.Customer).filter(models.Customer.customer_id == customer_id).first()
    if customer:
        db.delete(customer)
        db.commit()
        return True
    return False