import streamlit as st
import yfinance as yf
import google.generativeai as genai
import plotly.graph_objects as go

# --- 1. APIキーの設定 ---
if "gemini" in st.secrets:
    api_key = st.secrets["gemini"]["api_key"].strip()
    genai.configure(api_key=api_key)

st.set_page_config(page_title="AI投資分析ダッシュボード", layout="wide")
st.title("🤖 先生専用：AI自動投資分析アプリ")

# --- 2. AIによる自動分析ボタン ---
st.header("📊 本日の市況を分析")

if st.button('最新の市況をAIで分析する'):
    with st.spinner('AIが情報を整理しています...'):
        try:
            # 最新の 1.5 Flash モデルを正式な名前で呼び出し
            model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
            
            prompt = """
            あなたはプロの投資家です。本日（2026年2月27日）の最新の金融状況に基づき、
            以下の構成で鋭い分析を提供してください。
            1. 【日米市況】背景と本質
            2. 【相場サイクル】現在はどの局面か
            3. 【銘柄洞察】三菱重工、住友電工、関電工、東京応化、SWCCへのコメント
            """
            
            response = model.generate_content(prompt)
            st.markdown("---")
            st.success("分析が完了しました")
            st.markdown(response.text)
            st.markdown("---")
                
        except Exception as e:
            # エラーが起きた際、詳細を表示して原因を切り分けます
            st.error("AIとの通信に課題が発生しています。")
            st.info(f"技術的なエラー詳細: {e}")
            if "404" in str(e):
                st.warning("ヒント：Google側の『開通』がまだ完了していない可能性があります。1.0 Proモデルへの切り替えを検討するか、もう少し時間を置く必要があります。")

st.markdown("---")

# --- 3. 個別銘柄チャート ---
st.header("🔍 個別銘柄チャート")
tickers = {"三菱重工": "7011.T", "住友電工": "5802.T", "関電工": "1942.T", "東京応化": "4186.T", "SWCC": "5805.T"}
selection = st.selectbox("銘柄を選んでください", list(tickers.keys()))

data = yf.download(tickers[selection], period="5y", interval="1mo")
if not data.empty:
    fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high
