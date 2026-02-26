import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# アプリのタイトル
st.set_page_config(page_title="森を見て木を見る投資アプリ", layout="wide")
st.title("🌲 森を見て木を見る投資アプリ")

# --- 1. 森の分析（相場サイクルと詳細分析） ---
st.header("📊 現在の相場サイクルと市況分析")

# アメリカと日本を横に並べる設定
col_us, col_jp = st.columns(2)

with col_us:
    st.subheader("🇺🇸 アメリカ：【業績相場】")
    st.markdown("""
    **【AI実需への回帰とトランプリスク】**
    - **背景**: エヌビディア（NVDA）の好決算が「AIバブル崩壊論」を粉砕。昨夜の一般教書演説でトランプ大統領が「軍事増強」と「外交解決」のバランスに触れたことで、過度な地政学リスクが後退しました。
    - **相場の本質**: 「期待から実績への移行」。M7が「AIでどれだけ稼げるか」という疑念に対し、物理的なインフラ（データセンター）への支出を維持していることが確認されました。
    """)

with col_jp:
    st.subheader("🇯🇵 日本：【金融相場 ＋ 業績相場】")
    st.markdown("""
    **【高市トレードと最高値更新】**
    - **背景**: 高市首相による「利上げ難色」発言で、日銀の早期利上げ観測が後退（円安155-156円）。これが輸出株の採算向上と、ハイテク株への追い風になっています。
    - **相場の本質**: 「官製円安×インフラ特需」。米国が求めるAIインフラを支える部品・重工・電線において、日本が唯一無二のサプライヤーとして再評価されています。
    """)

st.markdown("---")

# --- 2. 木の分析（個別銘柄チャート） ---
st.header("🔍 注目の木（監視銘柄）")

# 監視銘柄のリスト
tickers = {
    "三菱重工 (7011.T)": "7011.T",
    "住友電工 (5802.T)": "5802.T",
    "関電工 (1942.T)": "1942.T",
    "東京応化 (4186.T)": "4186.T",
    "SWCC (5805.T)": "5805.T",
    "三井E&S (7003.T)": "7003.T"
}

selection = st.selectbox("銘柄を選んでください", list(tickers.keys()))
ticker_symbol = tickers[selection]

# データの取得（月足）
data = yf.download(ticker_symbol, period="5y", interval="1mo")

if not data.empty:
    # 月足チャートの作成
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'])])
    
    fig.update_layout(
        title=f"{selection} - 月足チャート",
        xaxis_rangeslider_visible=False,
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

    # 財務情報の簡易表示
    stock = yf.Ticker(ticker_symbol)
    info = stock.info
    st.subheader("🏦 財務・基本情報")
    c1, c2, c3 = st.columns(3)
    c1.metric("自己資本比率", f"{info.get('debtToEquity', 0)/100:.2f}%" if info.get('debtToEquity') else "データなし")
    c2.metric("配当利回り", f"{info.get('dividendYield', 0)*100:.2f}%" if info.get('dividendYield') else "無配")
    c3.metric("現在値", f"{info.get('currentPrice', 0)} 円")
else:
    st.error("データの取得に失敗しました。少し待ってから再読み込みしてください。")

st.markdown("---")
st.caption("2026年2月26日 最終更新：先生の思考アルゴリズムに基づき分析")
