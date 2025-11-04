import pandas as pd
from datetime import datetime, timedelta
from database import load_items, load_orders

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
