from fastapi import HTTPException
from .database import Session
from ..models import Customer

class CRUDCustomer:
    @staticmethod
    def create(session: Session, customer: Customer) -> Customer:
        session.add(customer)
        session.commit()
        session.refresh(customer)
        return customer

    @staticmethod
    def read(session: Session, customer_id: int) -> Customer:
        customer = session.get(Customer, customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer

    @staticmethod
    def delete(session: Session, customer_id: int) -> dict:
        customer = session.get(Customer, customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        session.delete(customer)
        session.commit()
        return {"message": f"Customer {customer_id} successfully deleted"}


crud_customer = CRUDCustomer()

