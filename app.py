import streamlit as st
import yfinance as yf
import google.generativeai as genai
import plotly.graph_objects as go

# 鍵を読み込む設定
try:
    # 登録されたAPIキーを直接読み込み
    key = st.secrets["gemini"]["api_key"]
    genai.configure(api_key=key) 
except Exception as e:
    st.error("APIキーの設定が見つかりません。Settings > Secrets を確認してください。")

st.set_page_config(page_title="AI投資分析ダッシュボード", layout="wide")
st.title("🤖 先生専用：AI自動投資分析アプリ")

# --- AIによる自動分析ボタン ---
if st.button('最新の市況をAIで分析する'):
    with st.spinner('Geminiが最新情報を分析中...'):
        try:
            # どんな環境(v1beta等)でも確実に存在する「gemini-pro」という名前を使用します
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = """
            あなたはプロの投資家です。本日（2026年2月26日）の最新の金融ニュースに基づき、以下の構成で分析してください。
            
            1. 【アメリカ市況分析】背景と、相場の本質
            2. 【日本市況分析】背景と、相場の本質
            3. 現在の相場サイクル（日米それぞれ：金融・業績・逆金融・逆業績相場から判定）
            4. セクター別の追い風（日米の注目業種）
            5. 個別銘柄ピック（三菱重工、住友電工、関電工、東京応化、SWCCの中から本日の推奨）
            
            専門用語を使いつつ、簡潔で分かりやすく、プロらしい洞察を含めてください。
            """
            
            # 安全な方法で生成を実行
            response = model.generate_content(prompt)
            st.markdown(response.text)
            
        except Exception as e:
            st.error("分析中にエラーが発生しました。")
            # エラーの具体的な中身を表示し、対策を立てやすくします
            st.info(f"技術的なエラー詳細: {e}")

st.markdown("---")

# --- 個別銘柄チャート ---
st.header("🔍 個別銘柄の確認")
tickers = {"三菱重工": "7011.T", "住友電工": "5802.T", "関電工": "1942.T", "東京応化": "4186.T", "SWCC": "5805.T"}
selection = st.selectbox("銘柄を選んでください", list(tickers.keys()))

data = yf.download(tickers[selection], period="5y", interval="1mo")
if not data.empty:
    fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'])])
    fig.update_layout(title=f"{selection} 月足チャート", xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

st.caption("2026年2月26日 運用開始")
