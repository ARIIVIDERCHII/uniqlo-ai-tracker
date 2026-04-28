import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

def train_predictive_model():
    print("🧠 Starting Machine Learning module...\n")
    
    
    conn = sqlite3.connect('uniqlo_prices.db')
    df = pd.read_sql_query("SELECT * FROM price_history", conn)
    conn.close()

    if len(df) < 100:
        print("Not enough data to train the model. Wait a few days for the spider to collect history!")
        return

    print(f"📊 Loaded {len(df)} records. Preparing data...")

    
    X = pd.get_dummies(df[['color', 'size', 'current_price']])

    
    df['is_scarce'] = df['stock_status'].apply(lambda x: 1 if x in ['LOW_STOCK', 'STOCK_OUT'] else 0)
    y = df['is_scarce']

    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    
    print("🌲 Training Random Forest model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    
    predictions = model.predict(X_test)
    
    print("\n✅ Testing Results (Shortage Prediction Accuracy):")
    print(classification_report(y_test, predictions, target_names=['In Stock', 'Shortage'], zero_division=0))
    
    
    feature_importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
    print("\n🔥 TOP-5 features influencing shortage (AI Analysis):")
    print(feature_importances.head(5))

if __name__ == "__main__":
    train_predictive_model()