from datetime import datetime
import os
import time
import streamlit as st

# إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="نظام السجل المدرسي - سلطنة عمان", page_icon="🇴🇲", layout="centered"
)

# حقن أكواد CSS بتأثير الزجاج الكامل (Glassmorphism)
st.markdown(
    """
    <style>
    @import url('https://googleapis.com');

    /* تطبيق الخط العربي واتجاه الصفحة وخلفية متدرجة لإبراز الزجاج */
    html, body, [class*="css"], [data-testid="stAppViewContainer"] {
        font-family: 'Tajawal', sans-serif !important;
        direction: rtl;
        text-align: right;
        background: linear-gradient(135deg, #dbeafe 0%, #eff6ff 45%, #e0e7ff 100%) !important;
        background-attachment: fixed !important;
    }

    /* إخفاء خلفية الهيدر الافتراضية لستريمليت */
    [data-testid="stHeader"] {
        background: transparent !important;
    }

    /* حركات الأنيميشن */
    @keyframes slideDown {
        from { opacity: 0; transform: translateY(-25px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulseGlow {
        0% { box-shadow: 0 0 0 0 rgba(212, 175, 55, 0.5); }
        70% { box-shadow: 0 0 0 12px rgba(212, 175, 55, 0); }
        100% { box-shadow: 0 0 0 0 rgba(212, 175, 55, 0); }
    }

    /* الترويسة الرسمية الزجاجية */
    .official-header {
        background: linear-gradient(135deg, rgba(10, 37, 64, 0.88) 0%, rgba(29, 99, 184, 0.82) 100%);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        padding: 30px 20px;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px rgba(10, 37, 64, 0.18);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-bottom: 4px solid #d4af37;
        animation: slideDown 0.8s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    .official-header .emblem-badge {
        font-size: 36px;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(8px);
        width: 75px;
        height: 75px;
        line-height: 75px;
        border-radius: 50%;
        margin: 0 auto 15px auto;
        display: block;
        border: 1.5px solid rgba(212, 175, 55, 0.7);
        animation: pulseGlow 2.5s infinite;
        transition: transform 0.3s ease;
    }
    .official-header .emblem-badge:hover {
        transform: scale(1.1) rotate(8deg);
    }
    .official-header h1 {
        margin: 0;
        font-size: 24px;
        font-weight: 800;
        color: #ffffff;
    }
    .official-header p {
        margin: 8px 0 0 0;
        font-size: 16px;
        color: #e2e8f0;
        font-weight: 500;
    }

    /* شريط الوقت والتاريخ الزجاجي */
    .time-banner {
        background: rgba(255, 255, 255, 0.55);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        padding: 14px 22px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.75);
        border-right: 5px solid #1d63b8;
        box-shadow: 0 8px 24px rgba(31, 38, 135, 0.06);
        margin-bottom: 22px;
        font-weight: 700;
        color: #0f172a;
        display: flex;
        justify-content: space-between;
        animation: fadeInUp 0.6s ease-out;
    }

    /* نموذج الإدخال الزجاجي */
    [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.6) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.8) !important;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.08) !important;
        animation: fadeInUp 0.8s ease-out;
    }

    /* حقول الإدخال بتأثير زجاجي خفيف */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.75) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.9) !important;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.04);
        transition: all 0.3s ease;
    }
    .stTextInput input:focus {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-color: #1d63b8 !important;
        box-shadow: 0 0 0 3px rgba(29, 99, 184, 0.15) !important;
    }

    /* الأزرار بتأثير زجاجي لامع */
    .stButton > button, .stFormSubmitButton > button, .stDownloadButton > button {
        width: 100%;
        background: linear-gradient(135deg, rgba(13, 59, 102, 0.92) 0%, rgba(29, 99, 184, 0.92) 100%) !important;
        backdrop-filter: blur(8px);
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        padding: 12px 24px !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 6px 20px rgba(29, 99, 184, 0.25) !important;
    }
    .stButton > button:hover, .stFormSubmitButton > button:hover, .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(29, 99, 184, 0.38) !important;
    }

    /* بطاقات عرض السجلات الزجاجية */
    .record-card {
        background: rgba(255, 255, 255, 0.58);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        padding: 16px 20px;
        border-radius: 16px;
        margin-bottom: 14px;
        border: 1px solid rgba(255, 255, 255, 0.75);
        box-shadow: 0 6px 20px rgba(31, 38, 135, 0.06);
        transition: transform 0.25s ease, box-shadow 0.25s ease, background 0.25s ease;
        animation: fadeInUp 0.5s ease-out;
    }
    .record-card:hover {
        transform: translateX(-5px);
        background: rgba(255, 255, 255, 0.8);
        box-shadow: 0 10px 28px rgba(31, 38, 135, 0.12);
    }
    .card-positive {
        border-right: 6px solid #10b981;
    }
    .card-negative {
        border-right: 6px solid #ef4444;
    }
    .badge-positive {
        background: rgba(209, 250, 229, 0.85);
        color: #065f46;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 700;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .badge-negative {
        background: rgba(254, 226, 226, 0.85);
        color: #991b1b;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 700;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }

    /* صندوق الإدارة الزجاجي */
    [data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.5) !important;
        backdrop-filter: blur(12px) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.7) !important;
    }
    </style>
    
    <!-- الترويسة -->
    <div class="official-header">
        <span class="emblem-badge">🇴🇲</span>
        <h1>سلطنة عمان - وزارة التربية والتعليم</h1>
        <p>نظام سجل المخالفات والتعزيزات المدرسية</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# جلب التاريخ والوقت
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")
current_time = now.strftime("%H:%M:%S")

st.markdown(
    f"""
    <div class="time-banner">
        <span>📅 التاريخ: {current_date}</span>
        <span>⏰ الوقت: {current_time}</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# نموذج إدخال البيانات
with st.form("data_form", clear_on_submit=True):
    st.markdown("### 📝 تسجيل بيان جديد")
    col1, col2 = st.columns(2)
    with col1:
        id_val = st.text_input("معرف الطالب (ID)", placeholder="مثال: 1024")
        type_val = st.selectbox("نوع السجل", ["تعزيز", "مخالفة"])
    with col2:
        class_val = st.text_input("الفصل (Class)", placeholder="مثال: 10/أ")
        details_val = st.text_input(
            "التفاصيل", placeholder="اكتب سبب المخالفة أو التعزيز"
        )

    submit_button = st.form_submit_button(label="💾 إضافة وحفظ السجل")

if submit_button:
    if id_val and details_val and class_val:
        entry = f"{type_val}|{id_val}|{details_val}|{current_date}|{current_time}|{class_val}\n"
        with open("R.txt", "a", encoding="utf-8") as f:
            f.write(entry)

        st.success("✅ تمت إضافة وحفظ البيانات بنجاح!")
        st.balloons()
        time.sleep(1.8)
        st.rerun()
    else:
        st.warning("⚠️ يرجى ملء جميع الحقول المطلوبة قبل الحفظ.")

st.divider()
st.subheader("📋 السجلات المحفوظة")

if os.path.exists("R.txt"):
    with open("R.txt", "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    if lines:
        # عرض السجلات كبطاقات زجاجية من الأحدث إلى الأقدم
        for line in reversed(lines):
            parts = line.split("|")
            if len(parts) == 6:
                r_type, r_id, r_details, r_date, r_time, r_class = parts
                card_class = (
                    "card-positive" if r_type == "تعزيز" else "card-negative"
                )
                badge_class = (
                    "badge-positive" if r_type == "تعزيز" else "badge-negative"
                )
                icon = "🌟" if r_type == "تعزيز" else "⚠️"

                st.markdown(
                    f"""
                    <div class="record-card {card_class}">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                            <span class="{badge_class}">{icon} {r_type}</span>
                            <span style="color: #475569; font-size: 13px; font-weight: 500;">📅 {r_date} | ⏰ {r_time}</span>
                        </div>
