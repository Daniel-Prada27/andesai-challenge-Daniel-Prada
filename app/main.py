from fastapi import FastAPI, HTTPException
from typing import Union
from models import Item, Order
from services import create_item, create_order, get_items, get_orders, get_stock_coverage, update_item

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

@app.get('/kpi/stock-coverage')
def read_stock_coverage(days: Union[int, None] = 7):
    try:
        return get_stock_coverage(days)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.put('/items/{sku}')
def updt_item(sku: str, item: Item):
    try:
        sku = update_item(sku, item)
        return {"message": f"Item {sku} updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
