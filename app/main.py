from fastapi import FastAPI, HTTPException
from models import Item, OrderItem, Order
from services import create_item, create_order, get_items, get_orders

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/items/")
def read_items():
    return get_items()

@app.get("/orders/")
def read_orders():
    return get_orders()

@app.post("/items/")
def add_item(item: Item):
    try:
        sku = create_item(item)
        return {"message": f"Item {sku} created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/orders/")
def add_order(order: Order):
    try:
        return create_order(order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))