from fastapi import APIRouter, HTTPException
from services.orders import get_orders, create_order
from models import Order

router = APIRouter()



@router.get("/orders")
def read_orders():
    return get_orders()

    
@router.post("/orders")
def add_order(order: Order):
    try:
        return create_order(order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))