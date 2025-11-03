import pandas as pd
from database import load_items, load_orders, save_items, save_orders

from models import Item, OrderItem, Order


def create_item(item):
    df = load_items()

    if (item.sku in df["sku"].values):
        raise ValueError(f"SKU {item.sku} already exists")

    new_item = pd.DataFrame([item.model_dump()])
    # new_item.head()

    df = pd.concat([df, new_item], ignore_index=True)
    save_items(df)
    return item.sku

def create_order(order):
    df_items = load_items()
    df_orders = load_orders()

    for item in order.items:
        if (item.sku not in df_items['sku'].values):
            raise ValueError(f"Product sku={item.sku} not found")
        
        stock = df_items.loc[df_items['sku'] == item.sku, 'stock'].squeeze()
        if (stock < item.qty):
            raise ValueError(f"Insufficient stock for product sku={item.sku}")
        
    total_cost = 0
    for item in order.items:
        data_idx = df_items.index[df_items["sku"] == item.sku][0]
        
        cost = df_items.loc[data_idx, 'unit_cost']

        total_cost += cost * item.qty

        df_items.loc[data_idx, 'stock'] -= item.qty

        new_order = {'order_id': order.order_id, "sku": item.sku, "qty": item.qty}

        new_order = pd.DataFrame([new_order])

        df_orders = pd.concat([df_orders, new_order], ignore_index=True)

    save_items(df_items)
    save_orders(df_orders)

    return {"order_id": order.order_id, "status": "success", "total_cost": float(total_cost)}

def get_items():
    df = load_items()
    return df.to_dict(orient='records')

def get_orders():
    df = load_orders()
    return df.to_dict(orient='records')