import sqlite3
import pandas as pd

def run_analytics():
    print("🧠 Starting Analytics Module (Pandas)...\n")
    
    conn = sqlite3.connect('uniqlo_prices.db')
    df = pd.read_sql_query("SELECT * FROM price_history", conn)
    conn.close()

    if df.empty:
        print("Database is empty! Run spider.py first.")
        return

    df['current_price'] = pd.to_numeric(df['current_price'], errors='coerce')
    
    total_variations = len(df)
    unique_products = df['product_id'].nunique()
    
    print(f"📊 GENERAL STATISTICS:")
    print(f"Unique jacket models: {unique_products}")
    print(f"Total color/size variations: {total_variations}")
    print(f"Average category price: ¥{df['current_price'].mean():.0f}\n")

    print("🔥 STOCK STATUSES:")
    stock_counts = df['stock_status'].value_counts()
    print(stock_counts.to_string())
    print("\n")

    low_stock_items = df[df['stock_status'].isin(['LOW_STOCK', 'STOCK_OUT'])]
    
    if not low_stock_items.empty:
        print("⚠️ WARNING! These items are running out (Buy Now Candidates):")
        deficit_profile = low_stock_items.groupby(['color', 'size']).size().reset_index(name='count')
        deficit_profile = deficit_profile.sort_values(by='count', ascending=False)
        print(deficit_profile.head(10).to_string(index=False))
    else:
        print("No current rush, all tracked items are IN_STOCK.")

if __name__ == "__main__":
    run_analytics()