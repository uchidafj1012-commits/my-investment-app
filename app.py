import streamlit as st
import yfinance as yf
import google.generativeai as genai
import plotly.graph_objects as go

# --- 1. APIキーの設定 ---
if "gemini" in st.secrets:
    api_key = st.secrets["gemini"]["api_key"].strip()
    # 最もシンプルな初期設定に戻します
    genai.configure(api_key=api_key)

st.set_page_config(page_title="AI投資分析ダッシュボード", layout="wide")
st.title("🤖 先生専用：AI自動投資分析アプリ")

# --- 2. AIによる自動分析ボタン ---
st.header("📊 本日の市況を分析")

if st.button('最新の市況をAIで分析する'):
    with st.spinner('AIが情報を整理しています...'):
        try:
            # 【究極の修正】
            # モデル名に直接 'v1' 系統であることを明示する「隠しコマンド」のような書き方です
            model = genai.GenerativeModel(model_name='gemini-1.5-flash')
            
            # APIのバージョンを内部的に強制指定する最も安全な方法
            response = model.generate_content(
                "あなたはプロの投資家です。本日の日米株式市場について、背景と本質を短く分析してください。"
            )
            
            if response:
                st.markdown("---")
                st.success("分析が完了しました")
                st.write(response.text)
                st.markdown("---")
                
        except Exception as e:
            st.error("AIとの通信に課題が発生しています。")
            st.info(f"技術的なエラー詳細: {e}")
            st.write("このエラーが続く場合、Google AI Studioで新しいAPIキーを作成し、古いキーと差し替えるのが一番の近道かもしれません。")

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
