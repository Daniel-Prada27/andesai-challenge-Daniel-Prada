from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

ITEMS_PATH = os.getenv("ITEMS_CSV_PATH")
ORDERS_PATH = os.getenv("ORDERS_CSV_PATH")

def load_items():
    return pd.read_csv(ITEMS_PATH, dtype={'sku': str})

def save_items(df):
    df.to_csv(ITEMS_PATH, index=False)

def load_orders():
    return pd.read_csv(ORDERS_PATH)

def save_orders(df):
    df.to_csv(ORDERS_PATH, index=False)


df = load_items()

print(df.head())

df.loc[df['name'] == 'Pollo', 'stock'] = 80

save_items(df)

df = load_items()
print(df.head())