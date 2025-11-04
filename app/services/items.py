import pandas as pd
from database import load_items, save_items

def create_item(item):
    df = load_items()

    if (item.sku in df["sku"].values):
        raise ValueError(f"SKU {item.sku} already exists")

    new_item = pd.DataFrame([item.model_dump()])

    df = pd.concat([df, new_item], ignore_index=True)
    save_items(df)
    return item.sku


def get_items():
    df = load_items()
    return df.to_dict(orient='records')


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