import requests
import sqlite3
import time
from datetime import datetime

CATALOG_URL = "https://www.uniqlo.com/jp/api/commerce/v5/ja/products?path=1072%2C1750%2C%2C&genderId=1072&offset=0&limit=36&imageRatio=3x4&rankingGender=men&rankingClassId=1750&httpFailure=true"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*"
}

def init_db():
    conn = sqlite3.connect('uniqlo_prices.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT,
            date_checked TEXT,
            color TEXT,
            size TEXT,
            current_price INTEGER,
            stock_status TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_to_db(product_id, color, size, price, stock_status):
    conn = sqlite3.connect('uniqlo_prices.db')
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO price_history (product_id, date_checked, color, size, current_price, stock_status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (product_id, now, color, size, price, stock_status))
    conn.commit()
    conn.close()

def get_product_ids():
    print("🌐 Requesting Catalog Master List...")
    response = requests.get(CATALOG_URL, headers=headers)
    
    product_ids = []
    if response.status_code == 200:
        data = response.json()
        items = data.get("result", {}).get("items", [])
        for item in items:
            pid = item.get("productId")
            if pid:
                product_ids.append(pid)
        product_ids = list(set(product_ids))
        print(f"🎯 Found unique products: {len(product_ids)}")
        return product_ids
    return []

def fetch_single_product(product_id):
    product_url = f"https://www.uniqlo.com/jp/api/commerce/v5/ja/products/{product_id}/price-groups/00/l2s?withPrices=true&withStocks=true&includePreviousPrice=false"
    
    response = requests.get(product_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        result_data = data.get("result", {})
        
        items = result_data.get("l2s", [])
        prices_dict = result_data.get("prices", {})
        stocks_dict = result_data.get("stocks", {})
        
        if not items:
            print(f"    [!] Server returned no data for {product_id}.")
            return
            
        saved_count = 0 
        for item in items:
            color = item.get("color", {}).get("displayCode", "N/A")
            size = item.get("size", {}).get("displayCode", "N/A")
            l2_id = item.get("l2Id")
            
            # Map Relational Data (Prices & Stocks)
            item_price_data = prices_dict.get(l2_id, {})
            base_price = item_price_data.get("base", {}).get("value", 0)
            
            promo_data = item_price_data.get("promo") or {}
            promo_price = promo_data.get("value", 0)
            
            current_price = promo_price if promo_price > 0 else base_price
            
            item_stock_data = stocks_dict.get(l2_id, {})
            stock_status = item_stock_data.get("statusCode", "Unknown")
            
            save_to_db(product_id, color, size, current_price, stock_status)
            saved_count += 1
            
        print(f"✅ Product {product_id} processed ({saved_count} variations saved).")
    else:
        print(f"⚠️ Error parsing product {product_id}")

if __name__ == "__main__":
    init_db()
    ids_to_scrape = get_product_ids()
    if ids_to_scrape:
        print("\n🚀 Starting mass data collection...")
        for i, pid in enumerate(ids_to_scrape):
            print(f"[{i+1}/{len(ids_to_scrape)}] Processing {pid}...")
            fetch_single_product(pid)
            time.sleep(2) 
        print("\n🎉 Data collection completed successfully!")