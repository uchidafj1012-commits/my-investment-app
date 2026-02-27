import streamlit as st
import requests
import json

# --- 1. APIキーの設定 ---
api_key = ""
if "gemini" in st.secrets:
    api_key = st.secrets["gemini"]["api_key"].strip()

st.set_page_config(page_title="AI投資分析", layout="wide")
st.title("🤖 先生専用：AI自動投資分析アプリ")

# --- 2. AI分析 ---
st.header("📊 本日の市況を分析")

if st.button('分析を実行する'):
    if not api_key:
        st.error("APIキーが設定されていません。")
    else:
        with st.spinner('AIが回答を生成中...'):
            # 【今回の修正点】URLの「v1」と「gemini-1.5-flash」の組み合わせを最新仕様に固定
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{"text": "あなたはプロの投資家です。2026年2月27日の株式市場について、日本とアメリカの状況を投資家視点で短く教えて。"}]
                }]
            }
            
            try:
                response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
                res_data = response.json()
                
                if response.status_code == 200:
                    answer = res_data['candidates'][0]['content']['parts'][0]['text']
                    st.success("分析が完了しました")
                    st.markdown("---")
                    st.write(answer)
                    st.markdown("---")
                else:
                    # エラーが出た場合、自動で「旧型モデル」で再試行する仕組みを追加
                    st.warning("最新モデルが準備中のため、安定版で再試行します...")
                    url_retry = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={api_key}"
                    response_retry = requests.post(url_retry, json=payload, headers={'Content-Type': 'application/json'})
                    
                    if response_retry.status_code == 200:
                        answer = response_retry.json()['candidates'][0]['content']['parts'][0]['text']
                        st.success("安定版モデルで分析を完了しました")
                        st.write(answer)
                    else:
                        st.error(f"Googleサーバーからエラーが返されました (Status: {response.status_code})")
                        st.json(res_data)
                    
            except Exception as e:
                st.error(f"通信に失敗しました: {e}")

st.markdown("---")
st.caption("2026年2月27日 運用中")
