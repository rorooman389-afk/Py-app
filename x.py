from datetime import datetime
import os
from zoneinfo import ZoneInfo
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
    @import url('https://googleapis.com');

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
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.07) !important;
    }

    .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.75) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.9) !important;
        transition: all 0.3s ease;
    }
    .stTextInput input:focus {
        background-color: rgba(255, 255, 255, 0.96) !important;
        border-color: #1d63b8 !important;
        box-shadow: 0 0 0 3px rgba(29, 99, 184, 0.15) !important;
    }

    .glass-record-card {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        padding: 15px 20px;
        border-radius: 15px;
        margin-bottom: 12px;
        border: 1px solid rgba(255, 255, 255, 0.8);
        box-shadow: 0 6px 18px rgba(31, 38, 135, 0.05);
        transition: transform 0.25s ease, background 0.25s ease;
    }
    .glass-record-card:hover {transform: translateX(-5px); background: rgba(255, 255, 255, 0.82);}
    .border-positive {border-right: 5px solid #10b981;}
    .border-negative {border-right: 5px solid #ef4444;}
    .border-neutral {border-right: 5px solid #1d63b8;}
    
    .pill-positive {
        background: rgba(209, 250, 229, 0.85);
        color: #065f46;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 700;
    }
    .pill-negative {
        background: rgba(254, 226, 226, 0.85);
        color: #991b1b;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 700;
    }

    .stButton > button, .stFormSubmitButton > button, .stDownloadButton > button {
        width: 100%;
        background: linear-gradient(135deg, rgba(13, 59, 102, 0.92) 0%, rgba(29, 99, 184, 0.92) 100%) !important;
        backdrop-filter: blur(8px) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 12px !important;
        padding: 11px 22px !important;
        font-weight: 700 !important;
        box-shadow: 0 6px 18px rgba(29, 99, 184, 0.25) !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover, .stFormSubmitButton > button:hover, .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(29, 99, 184, 0.38) !important;
    }
    </style>
    
    <div class="official-header">
        <span class="emblem-badge">🇴🇲</span>
        <h1>سلطنة عمان - وزارة التربية والتعليم</h1>
        <p>نظام سجل المخالفات والتعزيزات المدرسية</p>
    </div>
    """,
    unsafe_allow_html=True,
)


def render_card(line_text):
    parts = [p.strip() for p in line_text.split("|")]
    if len(parts) == 6:
        p1, p2, p3, p4, p5, p6 = parts
        r_type = p1.replace("النوع:", "").strip()
        r_id = p2.replace("المعرف:", "").strip()
        r_details = p3.replace("التفاصيل:", "").strip()
        r_date = p4.replace("التاريخ:", "").strip()
        r_time = p5.replace("الساعة:", "").strip()
        r_class = p6.replace("الفصل:", "").strip()

        is_pos = r_type == "تعزيز"
        b_cls = "border-positive" if is_pos else "border-negative"
        p_cls = "pill-positive" if is_pos else "pill-negative"
        icon = "🌟" if is_pos else "⚠️"

        html = f"""
        <div class="glass-record-card {b_cls}">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span class="{p_cls}">{icon} {r_type}</span>
                <span style="color: #475569; font-size: 13px;">📅 {r_date} | ⏰ {r_time}</span>
            </div>
            <div style="font-size: 16px; font-weight: 700; color: #0f172a; margin-bottom: 4px;">
                معرف الطالب: {r_id} &nbsp;•&nbsp; الفصل: {r_class}
            </div>
            <div style="color: #334155; font-size: 15px;">{r_details}</div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
    else:
        st.markdown(
            f'<div class="glass-record-card border-neutral">{line_text}</div>',
            unsafe_allow_html=True,
        )


violations_count = 0
reinforcements_count = 0
data = ""

if os.path.exists("R.txt"):
    with open("R.txt", "r", encoding="utf-8") as f:
        data = f.read()
    for line in data.splitlines():
        if "النوع: مخالفة" in line:
            violations_count += 1
        elif "النوع: تعزيز" in line:
            reinforcements_count += 1

total_records = violations_count + reinforcements_count

col1, col2, col3 = st.columns(3)
col1.metric(label="📊 إجمالي السجلات", value=total_records)
col2.metric(label="🌟 التعزيزات", value=reinforcements_count)
col3.metric(label="⚠️ المخالفات", value=violations_count)

st.write("")

now = datetime.now(ZoneInfo("Asia/Muscat"))
current_date = now.strftime("%Y-%m-%d")
current_time = now.strftime("%H:%M:%S")

st.info(f"📅 التاريخ الحالي: {current_date} | ⏰ الساعة الحالية: {current_time}")

with st.form("data_form", clear_on_submit=True):
    st.markdown("#### 📝 تسجيل بيان جديد")
