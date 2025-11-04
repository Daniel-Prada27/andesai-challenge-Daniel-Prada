from fastapi import APIRouter, HTTPException
from services.items import get_items, create_item, update_item, delete_item
from models import Item

router = APIRouter()

@router.get("/items")
def read_items():
    return get_items()

@router.post("/items")
def add_item(item: Item):
    try:
        sku = create_item(item)
        return {"message": f"Item {sku} created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put('/items/{sku}')
def updt_item(sku: str, item: Item):
    try:
        sku = update_item(sku, item)
        return {"message": f"Item {sku} updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete('/items/{sku}')
def remove_item(sku: str):
    try:
        sku = delete_item(sku)
        return {"message": f"Item {sku} deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))