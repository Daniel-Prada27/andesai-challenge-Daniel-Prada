from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    sku: str
    name: str
    stock: int
    unit_cost: float

class OrderItem(BaseModel):
    sku: str
    qty: int

class Order(BaseModel):
    order_id: str
    items: List[OrderItem]
