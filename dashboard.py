import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="Uniqlo AI Tracker", page_icon="🧥", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e6e6e6;
        padding: 5% 5% 5% 10%;
        border-radius: 12px;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease-in-out;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0px 8px 25px rgba(0, 0, 0, 0.1);
    }

    h1, h2, h3 {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #1a1a1a;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧥 Uniqlo AI Tracker / ユニクロ AIトラッカー")
st.markdown("**Data Pipeline:** Scraping ➔ SQLite ➔ Pandas ➔ Streamlit & Plotly")


@st.cache_data
def load_data():
    conn = sqlite3.connect('uniqlo_prices.db')
    df = pd.read_sql_query("SELECT * FROM price_history", conn)
    conn.close()
    
    
    status_translation = {
        'IN_STOCK': '在庫あり (In Stock)',
        'STOCK_OUT': '品切れ (Out of Stock)',
        'LOW_STOCK': '残りわずか (Low Stock)',
        'Неизвестно': '不明 (Unknown)'
    }
    
    
    df['status_display'] = df['stock_status'].map(status_translation)
    return df

df = load_data()

if df.empty:
    st.warning("⚠️ データベースが空です。先にクローラーを実行してください (Database is empty. Run spider first).")
else:
  
    tab1, tab2 = st.tabs(["📊 ダッシュボード (Dashboard)", "🤖 AI予測データ (AI Insights)"])

    
    with tab1:
        st.header("📈 今日のサマリー (Today's Summary)")
        
        
        total_items = len(df)
        in_stock = len(df[df['stock_status'] == 'IN_STOCK'])
        stock_out = len(df[df['stock_status'] == 'STOCK_OUT'])
        low_stock = len(df[df['stock_status'] == 'LOW_STOCK'])
        
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("総バリエーション (Total Variations)", total_items)
        col2.metric("在庫あり (In Stock)", in_stock)
        col3.metric("品切れ (Out of Stock)", stock_out)
        col4.metric("残りわずか (Low Stock)", low_stock, delta="- 要注意 (Warning)", delta_color="inverse")

        st.divider()

        
        st.header("🔍 不足状況の分析 (Deficit Analysis)")
        
        deficit_df = df[df['stock_status'].isin(['LOW_STOCK', 'STOCK_OUT'])]
        
        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:
            st.subheader("サイズ別の品切れ (Shortage by Size)")
            size_counts = deficit_df['size'].value_counts().reset_index()
            size_counts.columns = ['Size', 'Count']
            
            
            fig_size = px.bar(size_counts, x='Size', y='Count', text='Count', 
                              color_discrete_sequence=['#ed1d24'])
            fig_size.update_traces(textposition='outside')
            
            fig_size.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_size, use_container_width=True)

        with col_chart2:
            st.subheader("カラー別の品切れ (Shortage by Color)")
            color_counts = deficit_df['color'].value_counts().reset_index()
            color_counts.columns = ['Color', 'Count']
            
            
            fig_color = px.pie(color_counts, values='Count', names='Color', hole=0.4,
                               color_discrete_sequence=px.colors.sequential.RdBu)
            fig_color.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_color, use_container_width=True)

    
    with tab2:
        st.header("⚠️ 購入のシグナル (Buy Now Signal)")
        st.markdown("アルゴリズムが以下の商品の品切れを予測しています。(The algorithm predicts these items will sell out soon.)")
        
        
        buy_now_df = df[df['stock_status'] == 'LOW_STOCK'][['product_id', 'color', 'size', 'current_price', 'status_display']]
        
        
        buy_now_df.columns = ['商品ID (Product ID)', 'カラー (Color)', 'サイズ (Size)', '価格 (Price ¥)', 'ステータス (Status)']
        
        if not buy_now_df.empty:
            st.dataframe(buy_now_df, use_container_width=True, hide_index=True)
        else:
            st.success("現在、在庫不足の商品はありません。(All monitored items are currently in stock.)")