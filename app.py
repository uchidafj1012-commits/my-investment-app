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
    with st.spinner('AIが情報を整理しています...（開通直後は時間がかかる場合があります）'):
        try:
            # 最新の 1.5 Flash モデルを使用
            # 'models/' を頭につけることで、Google側に「正式な場所にあるモデルだよ」と再認識させます
model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
            
            prompt = """
            あなたはプロの投資家です。本日（2026年2月27日）の最新の金融状況に基づき、
            日本とアメリカの市況、注目銘柄（三菱重工、住友電工、関電工、東京応化、SWCC）についての洞察を述べてください。
            """
            
            response = model.generate_content(prompt)
            st.markdown("---")
            st.markdown(response.text)
            st.markdown("---")
                
        except Exception as e:
            st.error("現在、GoogleのAIサーバーが開通処理を行っています。")
            st.info(f"技術的なエラー詳細: {e}")
            st.write("※APIキー作成後、完全に有効化されるまで1時間程度かかる場合があります。このまましばらくお待ちください。")

st.markdown("---")

# --- 3. 個別銘柄チャート ---
st.header("🔍 個別銘柄チャート")
tickers = {"三菱重工": "7011.T", "住友電工": "5802.T", "関電工": "1942.T", "東京応化": "4186.T", "SWCC": "5805.T"}
selection = st.selectbox("銘柄を選んでください", list(tickers.keys()))

data = yf.download(tickers[selection], period="5y", interval="1mo")
if not data.empty:
    fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'])])
    fig.update_layout(title=f"{selection} 月足チャート", xaxis_rangeslider_visible=False, height=500)
    st.plotly_chart(fig, use_container_width=True)

st.caption("2026年2月27日 運用中")
