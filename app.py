import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# アプリのタイトル
st.set_page_config(page_title="森を見て木を見る投資アプリ", layout="wide")
st.title("🌲 森を見て木を見る投資アプリ")

# --- 1. 森の分析（相場サイクル） ---
st.header("📊 現在の相場サイクル")
col1, col2 = st.columns(2)
with col1:
    st.info("🇺🇸 アメリカ：【業績相場】")
    st.write("高金利を企業の稼ぐ力（EPS）が上回る。AI・公共事業が主役。")
with col2:
    st.success("🇯🇵 日本：【金融相場 ＋ 業績相場】")
    st.write("円安と国策（インフラ・防衛）のダブルメリット。")

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

# データの取得
data = yf.download(ticker_symbol, period="2y", interval="1mo")

if not data.empty:
    # 月足チャートの作成
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'])])
    
    fig.update_layout(title=f"{selection} - 月足チャート", xaxis_rangeslider_visible=False)
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
    st.error("データの取得に失敗しました。")

st.markdown("---")
st.caption("2026年2月26日時点の思考アルゴリズムに基づき生成")
