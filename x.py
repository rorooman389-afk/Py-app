from datetime import datetime, timezone, timedelta
import os
import streamlit as st

st.set_page_config(page_title="نظام السجل المدرسي", page_icon="🇴🇲", layout="centered")

if "show_balloons" not in st.session_state:
    st.session_state.show_balloons = False

if st.session_state.show_balloons:
    st.balloons()
    st.session_state.show_balloons = False

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    html, body, [class*="css"], [data-testid="stAppViewContainer"] {
        font-family: 'Tajawal', sans-serif !important;
        direction: rtl;
        text-align: right;
        background-color: #e8f0fe !important;
        background-image: 
            radial-gradient(at 15% 15%, rgba(29, 99, 184, 0.22) 0px, transparent 50%),
            radial-gradient(at 85% 25%, rgba(16, 185, 129, 0.16) 0px, transparent 50%),
            radial-gradient(at 50% 85%, rgba(212, 175, 55, 0.18) 0px, transparent 55%) !important;
        background-attachment: fixed !important;
        animation: fadeIn 0.8s ease-in-out;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stHeader"] {background: transparent !important;}
    [data-testid="stToolbar"] {display: none !important;}

    .stTextInput, .stSelectbox, .stTextArea, .stButton, .stDownloadButton {
        direction: rtl;
        text-align: right;
    }

    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.58) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        padding: 16px !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.8) !important;
        box-shadow: 0 8px 24px rgba(31, 38, 135, 0.06) !important;
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        background: rgba(255, 255, 255, 0.8) !important;
        box-shadow: 0 12px 28px rgba(31, 38, 135, 0.12) !important;
    }
    [data-testid="column"]:nth-of-type(1) [data-testid="stMetric"] {border-right: 5px solid #1d63b8 !important;}
    [data-testid="column"]:nth-of-type(2) [data-testid="stMetric"] {border-right: 5px solid #10b981 !important;}
    [data-testid="column"]:nth-of-type(3) [data-testid="stMetric"] {border-right: 5px solid #ef4444 !important;}

    .official-header {
        background: linear-gradient(135deg, rgba(13, 59, 102, 0.88) 0%, rgba(29, 99, 184, 0.84) 100%);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        padding: 25px;
        border-radius: 18px;
        text-align: center;
        color: white;
        margin-bottom: 22px;
        box-shadow: 0 8px 32px rgba(10, 37, 64, 0.16);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-bottom: 4px solid #d4af37;
        animation: fadeIn 1s ease-in-out;
    }
    .official-header .emblem-badge {
        font-size: 32px;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(8px);
        width: 68px;
        height: 68px;
        line-height: 68px;
        border-radius: 50%;
        margin: 0 auto 12px auto;
        display: block;
        border: 1.5px solid rgba(212, 175, 55, 0.65);
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
        transition: transform 0.3s ease;
    }
    .official-header .emblem-badge:hover {transform: scale(1.1) rotate(5deg);}
    .official-header h1 {margin: 0; font-size: 22px; font-weight: 800; color: #ffffff;}
    .official-header p {margin: 8px 0 0 0; font-size: 15px; color: #f1f1f1; letter-spacing: 0.5px;}

    [data-testid="stAlert"] {
        background: rgba(255, 255, 255, 0.58) !important;
        backdrop-filter: blur(14px) !important;
        -webkit-backdrop-filter: blur(14px) !important;
        border: 1px solid rgba(255, 255, 255, 0.78) !important;
        border-right: 5px solid #1d63b8 !important;
        border-radius: 14px !important;
        box-shadow: 0 6px 20px rgba(31, 38, 135, 0.05) !important;
        color: #0f172a !important;
    }

    [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.6) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        padding: 25px !important;
        border-radius: 18px !important;
        border: 1px solid rgba(255, 255, 255, 0.85) !important;
        box-shadow: 0 8px 32px rgba(
