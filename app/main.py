from fastapi import FastAPI
from routers import items, orders, kpi

app = FastAPI()

app.include_router(items.router)
app.include_router(orders.router)
app. include_router(kpi.router)

@app.get("/")
def root():
    return {"message": "Mini-API de Operaciones de Restaurante"}
