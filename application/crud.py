from fastapi import HTTPException
from sqlmodel import Session
from .database import engine
from .models import CustomerDB, CustomerRead

class CRUDCustomer():
    
    @staticmethod
    def create(customer:CustomerDB) -> CustomerDB:
        with Session(engine) as session:
            session.add(customer)
            session.commit()
            session.refresh(customer)
            return customer
        
    @staticmethod      
    def read(customer_id:int) -> CustomerDB:
        with Session(engine) as session:
            customer = session.get(CustomerDB, customer_id)
            if not customer:
                raise HTTPException(status_code=404, detail="Customer not found")
            return customer

    @staticmethod
    def delete(customer_id:int) -> dict:
        with Session(engine) as session:
            customer = session.get(CustomerDB, customer_id)
            if not customer:
                raise HTTPException(status_code=404, detail="Customer not found")
            session.delete(customer)
            session.commit()
            return {"message" : f"Customer {customer_id} successfully deleted"}
        
crud_customer = CRUDCustomer()