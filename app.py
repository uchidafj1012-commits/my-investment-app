import streamlit as st
import yfinance as yf
import google.generativeai as genai
import plotly.graph_objects as go

# --- 1. APIキーの設定（最もシンプルな接続方式） ---
try:
    if "gemini" in st.secrets and "api_key" in st.secrets["gemini"]:
        api_key = st.secrets["gemini"]["api_key"]
        # 余計な設定を省き、最も標準的な方法で接続します
        genai.configure(api_key=api_key)
    else:
        st.error("Secretsの設定が正しくありません。[gemini] api_key の形式で保存してください。")
except Exception as e:
    st.error(f"設定エラー: {e}")

st.set_page_config(page_title="AI投資分析ダッシュボード", layout="wide")
st.title("🤖 先生専用：AI自動投資分析アプリ")

# --- 2. AIによる自動分析ボタン ---
st.header("📊 本日の森（相場全体）を分析")

if st.button('最新の市況をAIで分析する'):
    with st.spinner('AIが最新情報を分析中...'):
        try:
            # 【解決の鍵】 'models/' をつけない、最もプレーンな名前で呼び出します
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = """
            あなたはプロの投資家です。本日（2026年2月26日）の最新の金融ニュースに基づき、以下の構成で分析してください。
            
            1. 【アメリカ市況分析】背景と、相場の本質
            2. 【日本市況分析】背景と、相場の本質
            3. 現在の相場サイクル（日米それぞれ：金融・業績・逆金融・逆業績相場から判定）
            4. セクター別の追い風（日米の注目業種）
            5. 個別銘柄ピック（三菱重工、住友電工、関電工、東京応化、SWCCの中から推奨）
            """
            
            # 通信を開始
            response = model.generate_content(prompt)
            
            if response.text:
                st.markdown("---")
                st.markdown(response.text)
                st.markdown("---")
            else:
                st.warning("AIからの回答が空でした。もう一度お試しください。")
                
        except Exception as e:
            st.error("現在、GoogleのAIサーバーと接続を確認中です。")
            st.info(f"技術的なエラー詳細: {e}")
            st.write("※このエラーが続く場合、APIキーが『Gemini API』としてではなく『Google Cloud』用として発行されている可能性があります。")

st.markdown("---")

# --- 3. 個別銘柄チャート ---
st.header("🔍 個別銘柄（木）の確認")
tickers = {"三菱重工": "7011.T", "住友電工": "5802.T", "関電工": "1942.T", "東京応化": "4186.T", "SWCC": "5805.T"}
selection = st.selectbox("銘柄を選んでください", list(tickers.keys()))

data = yf.download(tickers[selection], period="5y", interval="1mo")
if not data.empty:
    fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'])])
    fig.update_layout(title=f"{selection} 月足チャート", xaxis_rangeslider_visible=False, height=500)
    st.plotly_chart(fig, use_container_width=True)

st.caption("2026年2月26日 運用開始")
