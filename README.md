# 🧥 Uniqlo AI Tracker & Predictor
**ユニクロ AI価格・在庫トラッカー**

An automated Data Engineering pipeline and Machine Learning dashboard built to track Uniqlo clothing inventory, detect shortages, and predict the best time to buy using Scikit-Learn.

## 🚀 Features
* **Automated Web Scraper:** Bypasses basic API protections to fetch real-time price and stock data.
* **ETL Pipeline:** Cleans and normalizes relational JSON data into a robust SQLite database.
* **Machine Learning:** Utilizes `RandomForestClassifier` to analyze historical data and identify key factors leading to stock shortages.
* **Interactive Dashboard:** A bilingual (ENG/JP) responsive UI built with Streamlit and Plotly for real-time data visualization.

## 🛠️ Tech Stack
* **Backend:** Python, Requests, SQLite3
* **Data Science:** Pandas, Scikit-Learn
* **Frontend:** Streamlit, Plotly Express
* **Automation:** Windows Task Scheduler / Cron

## 📦 Installation & Setup

1. Clone the repository:
   ```bash
   git clone [https://github.com/ARIIVIDERCHII/uniqlo-ai-tracker.git](https://github.com/ARIIVIDERCHII/uniqlo-ai-tracker.git)
   cd uniqlo-ai-tracker
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Data Pipeline (Collect initial data):
   ```bash
   python spider.py
   ```

4. Launch the Dashboard:
   ```bash
   streamlit run dashboard.py
   ```

## 🧠 ML Model Architecture
The project employs a Random Forest model with One-Hot Encoding for categorical features (`color`, `size`). It solves an imbalanced classification problem to predict the `LOW_STOCK` signal, revealing that variables like specific promotional prices and certain sizes (e.g., Japanese 'M' and 'L') have the highest feature importance in predicting shortages.

## 📝 License
This project is for educational and portfolio purposes only. Not affiliated with Uniqlo or Fast Retailing Co., Ltd.

---

# 🧥 ユニクロ AIトラッカー & 価格予測 (Uniqlo AI Tracker & Predictor)

ユニクロの衣類在庫を追跡し、品切れを検知して、Scikit-Learnを用いて最適な購入タイミングを予測する、自動化されたデータエンジニアリング・パイプラインおよび機械学習ダッシュボードです。

## 🚀 主な機能
* **自動ウェブスクレイパー:** APIの基本的な制限を適切に処理し、リアルタイムの価格および在庫データを取得します。
* **ETLパイプライン:** 取得したJSONデータをクレンジング・正規化し、堅牢なSQLiteデータベースに保存します。
* **機械学習予測:** `RandomForestClassifier`（ランダムフォレスト）を活用して過去のデータを分析し、在庫不足を引き起こす主な要因を特定します。
* **インタラクティブ・ダッシュボード:** StreamlitとPlotlyで構築された、リアルタイムでデータを可視化するバイリンガル（日英対応）のレスポンシブUI。

## 🛠️ 技術スタック
* **バックエンド:** Python, Requests, SQLite3
* **データサイエンス:** Pandas, Scikit-Learn
* **フロントエンド:** Streamlit, Plotly Express
* **自動化:** Windows タスクスケジューラ / Cron

## 📦 環境構築と実行方法

1. リポジトリのクローン:
   ```bash
   git clone [https://github.com/ARIIVIDERCHII/uniqlo-ai-tracker.git](https://github.com/ARIIVIDERCHII/uniqlo-ai-tracker.git)
   cd uniqlo-ai-tracker
   ```

2. 必要なパッケージのインストール:
   ```bash
   pip install -r requirements.txt
   ```

3. データパイプラインの実行（初期データの収集）:
   ```bash
   python spider.py
   ```

4. ダッシュボードの起動:
   ```bash
   streamlit run dashboard.py
   ```

## 🧠 機械学習モデルのアーキテクチャ
本プロジェクトでは、カテゴリ変数（`color`、`size`）に対するOne-Hotエンコーディングとランダムフォレストモデルを採用しています。不均衡データ（Imbalanced Data）の分類問題を処理して `LOW_STOCK`（残りわずか）のシグナルを予測し、特定のプロモーション価格や特定のサイズ（日本のMサイズやLサイズなど）が品切れ予測において最も重要度（Feature Importance）が高いことを明らかにしています。

## 📝 免責事項 (Disclaimer)
本プロジェクトは教育およびポートフォリオ目的でのみ作成されたものであり、株式会社ユニクロおよび株式会社ファーストリテイリングとは一切関係ありません。