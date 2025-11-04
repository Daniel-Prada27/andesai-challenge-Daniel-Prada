import pandas as pd
from datetime import datetime, timedelta
from database import load_items, load_orders, save_items, save_orders

from models import Item, OrderItem, Order


def create_item(item):
    df = load_items()

    if (item.sku in df["sku"].values):
        raise ValueError(f"SKU {item.sku} already exists")

    new_item = pd.DataFrame([item.model_dump()])

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

        current_date = datetime.now().date()
        new_order = {'order_id': order.order_id, "sku": item.sku, "qty": item.qty, "date": current_date}

        new_order = pd.DataFrame([new_order])

        df_orders = pd.concat([df_orders, new_order], ignore_index=True)
        df_orders['date'] = pd.to_datetime(df_orders['date'], errors='coerce').dt.strftime('%Y-%m-%d')

    save_items(df_items)
    save_orders(df_orders)

    return {"order_id": order.order_id, "status": "success", "total_cost": float(total_cost)}

def get_items():
    df = load_items()
    return df.to_dict(orient='records')

def get_orders():
    df = load_orders()
    return df.to_dict(orient='records')

def get_stock_coverage(days: int = 7):

    if days < 1:
        raise ValueError("Cannot query negative dates")

    df_items = load_items()
    df_orders = load_orders()

    if df_orders.empty:
        return {"message": "No orders recorded yet", "coverage": []}
    if df_items.empty:
        return {"message": "No items recorded yet", "coverage": []}

    start_date = datetime.now().date() - timedelta(days=days)

    today = datetime.now()
    start_date = today - timedelta(days=7)
    start_date = start_date.date()
    df_orders['date'] = df_orders['date'].dt.date

    filtered = df_orders[(df_orders["date"] >= start_date) & (df_orders["date"] < today.date())]

    sales = filtered.groupby("sku")['qty'].sum().reset_index()
    sales['avg_daily_sales'] = sales['qty'] / 7

    kpi_df = pd.merge(df_items, sales, how='left', on='sku').fillna(0)

    def get_stock_coverage(row):
        if row["avg_daily_sales"] > 0:
            return int(row["stock"] / row["avg_daily_sales"])
        return 0
    
    kpi_df['stock_coverage_in_days'] = kpi_df.apply(get_stock_coverage, axis=1)

    kpi_df = kpi_df[['sku', 'name', 'stock', 'avg_daily_sales', 'stock_coverage_in_days']].to_dict(orient='records')

    return kpi_df

def update_item(sku, item):
    df = load_items()

    if (sku not in df['sku'].values):
        raise ValueError(f"Product sku={sku} not found")

    df.loc[df['sku'] == sku, ['name', 'stock', 'unit_cost']] = [item.name, item.stock, item.unit_cost]

    save_items(df)

    return sku

def delete_item(sku):
    df = load_items()

    if (sku not in df['sku'].values):
        raise ValueError(f"Product sku={sku} not found")
    
    df = df[df['sku'] != sku]

    save_items(df)

    return sku