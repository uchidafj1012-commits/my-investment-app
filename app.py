import streamlit as st
import yfinance as yf
import google.generativeai as genai
import plotly.graph_objects as go

# --- 1. APIキーの設定 ---
if "gemini" in st.secrets:
    api_key = st.secrets["gemini"]["api_key"].strip()
    
    # 【ここが最重要修正】v1beta(テスト版)ではなくv1(正式版)の道を使うよう指定します
    client_options = {"api_version": "v1"}
    genai.configure(api_key=api_key, transport='rest', client_options=client_options)

st.set_page_config(page_title="AI投資分析ダッシュボード", layout="wide")
st.title("🤖 先生専用：AI自動投資分析アプリ")

# --- 2. AIによる自動分析ボタン ---
st.header("📊 本日の市況を分析")

if st.button('最新の市況をAIで分析する'):
    with st.spinner('AIが情報を整理しています...'):
        try:
            # 正式版の道を通るので、モデル名も標準のものに戻します
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = "あなたはプロの投資家です。本日の日米株式市場について、背景と本質を短く分析してください。"
            
            response = model.generate_content(prompt)
            
            if response:
                st.markdown("---")
                st.success("分析が完了しました")
                st.write(response.text)
                st.markdown("---")
                
        except Exception as e:
            st.error("AIとの通信に課題が発生しています。")
            st.info(f"技術的なエラー詳細: {e}")

st.markdown("---")

# --- 3. 個別銘柄チャート ---
st.header("🔍 個別銘柄チャート")
tickers = {"三菱重工": "7011.T", "住友電工": "5802.T", "関電工": "1942.T", "東京応化": "4186.T", "SWCC": "5805.T"}
selection = st.selectbox("銘柄を選んでください", list(tickers.keys()))

data = yf.download(tickers[selection], period="5y", interval="1mo")

if not data.empty:
    fig = go.Figure(data=[go.Candlestick(
        x=data.index, 
        open=data['Open'], 
        high=data['High'], 
        low=data['Low'], 
        close=data['Close']
    )])
    fig.update_layout(title=f"{selection} 月足チャート", xaxis_rangeslider_visible=False, height=500)
    st.plotly_chart(fig, use_container_width=True)

st.caption("2026年2月27日 運用中")
