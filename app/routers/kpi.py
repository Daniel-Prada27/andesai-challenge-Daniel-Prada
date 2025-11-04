from fastapi import APIRouter, HTTPException
from typing import Union
from services.kpi import get_stock_coverage

router = APIRouter()

@router.get('/kpi/stock-coverage')
def read_stock_coverage(days: Union[int, None] = 7):
    try:
        return get_stock_coverage(days)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))