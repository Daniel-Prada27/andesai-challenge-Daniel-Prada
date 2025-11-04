import pandas as pd
from datetime import datetime
from database import load_items, load_orders, save_items, save_orders


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

        current_date = datetime.now().date()
        new_order = {'order_id': order.order_id, "sku": item.sku, "qty": item.qty, "date": current_date}

        new_order = pd.DataFrame([new_order])

        df_orders = pd.concat([df_orders, new_order], ignore_index=True)
        df_orders['date'] = pd.to_datetime(df_orders['date'], errors='coerce').dt.strftime('%Y-%m-%d')

    save_items(df_items)
    save_orders(df_orders)

    return {"order_id": order.order_id, "status": "success", "total_cost": float(total_cost)}


def get_orders():
    df = load_orders()
    df['date'] = df['date'].dt.date
    return df.to_dict(orient='records')
