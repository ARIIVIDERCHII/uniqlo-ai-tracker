import requests
import json
import sqlite3
from datetime import datetime

API_URL = "https://www.uniqlo.com/jp/api/commerce/v5/ja/products/E484484-000/price-groups/00/l2s?withPrices=true&withStocks=true&includePreviousPrice=false&httpFailure=true"
PRODUCT_ID = "E484484" 

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
    print("🗄️ Database is ready!")

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

def fetch_uniqlo_data():
    print("Sending request to Uniqlo API...")
    response = requests.get(API_URL, headers=headers)

    if response.status_code == 200:
        data = response.json()
        items = data.get("result", {}).get("l2s", [])
        
        print("--- Saving data to DB ---")
        for item in items:
            color_code = item.get("color", {}).get("displayCode", "N/A")
            size_code = item.get("size", {}).get("displayCode", "N/A")
            
            prices = item.get("prices", {})
            base_price = prices.get("base", {}).get("value", 0)
            promo_price = prices.get("promo", {}).get("value", 0)
            current_price = promo_price if promo_price else base_price
            
            stocks = item.get("stocks", {})
            stock_status = stocks.get("status", "Unknown")
            
            save_to_db(PRODUCT_ID, color_code, size_code, current_price, stock_status)
            
        print("✅ All product variations successfully saved to the database!")
            
    else:
        print(f"❌ Error! Server code: {response.status_code}")

if __name__ == "__main__":
    init_db() 
    fetch_uniqlo_data()