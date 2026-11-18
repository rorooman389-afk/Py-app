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

    .official
