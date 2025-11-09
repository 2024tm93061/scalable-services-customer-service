from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
import csv

from app.database import SessionLocal, engine, Base
from app import crud, models


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Customer Service")


class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    kyc_status: Optional[str] = "PENDING"


class CustomerUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    kyc_status: Optional[str]


class CustomerOut(CustomerCreate):
    customer_id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def seed_db():
    db = SessionLocal()
    try:
        existing = db.query(models.Customer).first()
        if existing:
            return
        # seed from CSV
        try:
            with open("./customers.csv", newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # map CSV fields to model
                    data = {
                        "customer_id": int(row.get("customer_id")) if row.get("customer_id") else None,
                        "name": row.get("name"),
                        "email": row.get("email"),
                        "phone": row.get("phone"),
                        "kyc_status": row.get("kyc_status") or "PENDING",
                        "created_at": None,
                    }
                    # try parse created_at
                    created = row.get("created_at")
                    if created:
                        try:
                            data["created_at"] = datetime.fromisoformat(created)
                        except Exception:
                            try:
                                data["created_at"] = datetime.strptime(created, "%Y-%m-%d %H:%M:%S")
                            except Exception:
                                data["created_at"] = None
                    # do not pass customer_id None
                    if data.get("customer_id") is None:
                        data.pop("customer_id", None)
                    crud.create_customer(db, data)
        except FileNotFoundError:
            # no seed file provided; skip
            return
    finally:
        db.close()


@app.post("/customers/", response_model=CustomerOut)
def add_customer(customer: CustomerCreate, db=Depends(get_db)):
    data = customer.dict()
    created = crud.create_customer(db=db, customer_data=data)
    return created


@app.get("/customers/{customer_id}", response_model=CustomerOut)
def read_customer(customer_id: int, db=Depends(get_db)):
    customer = crud.get_customer(db=db, customer_id=customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@app.get("/customers/", response_model=List[CustomerOut])
def list_customers(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    return crud.get_customers(db=db, skip=skip, limit=limit)


@app.put("/customers/{customer_id}", response_model=CustomerOut)
def update_customer_info(customer_id: int, customer: CustomerUpdate, db=Depends(get_db)):
    updates = {k: v for k, v in customer.dict().items() if v is not None}
    updated = crud.update_customer(db=db, customer_id=customer_id, updates=updates)
    if updated is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return updated


@app.delete("/customers/{customer_id}", response_model=dict)
def delete_customer_info(customer_id: int, db=Depends(get_db)):
    ok = crud.delete_customer(db=db, customer_id=customer_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"detail": "Customer deleted"}