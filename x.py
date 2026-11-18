from datetime import datetime, timezone, timedelta
import os
import streamlit as st

st.set_page_config(page_title="نظام السجل المدرسي", page_icon="🇴🇲", layout="centered")

if "show_balloons" not in st.session_state:
    st.session_state.show_balloons = False

if st.session_state.show_balloons:
    st.balloons()
    st.session_state.show_balloons = False

CSS_STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');

html, body, [class*="css"], [data-testid="stAppViewContainer"] {
    font-family: 'Tajawal', sans-serif !important;
    direction: rtl;
    text-align: right;
    background-color: #e8f0fe !important;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stHeader"] {background: transparent !important;}

.official-header {
    background: linear-gradient(135deg, #0d3b66 0%, #1d63b8 100%);
    padding: 25px;
    border-radius: 18px;
    text-align: center;
    color: white;
    margin-bottom: 22px;
    border-bottom: 4px solid #d4af37;
}

.official-header .emblem-badge {
    font-size: 32px;
    background: rgba(255, 255, 255, 0.15);
    width: 68px;
    height: 68px;
    line-height: 68px;
    border-radius: 50%;
    margin: 0 auto 12px auto;
    display: block;
    border: 1.5px solid rgba(212, 175, 55, 0.65);
}

.glass-record-card {
    background: rgba(255, 255, 255, 0.8);
    padding: 15px 20px;
    border-radius: 15px;
    margin-bottom: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}
.border-positive {border-right: 5px solid #10b981;}
.border-negative {border-right: 5px solid #ef4444;}
.border-neutral {border-right
