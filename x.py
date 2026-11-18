from datetime import datetime
import os
from zoneinfo import ZoneInfo
import streamlit as st

st.set_page_config(page_title="نظام السجل المدرسي", page_icon="🇴🇲", layout="centered")

# تهيئة حالة الجلسة لإظهار البالونات بعد إعادة تحميل الصفحة
if "show_balloons" not in st.session_state:
    st.session_state.show_balloons = False

if st.session_state.show_balloons:
    st.balloons()
    st.session_state.show_balloons = False

# تصميم الواجهة بتأثير الزجاج (Glassmorphism) ودعم اللغة العربية
st.markdown(
    """
    <style>
    @import url('https://googleapis.com');

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* تطبيق الخط وخلفية متدرجة لإبراز تأثير الزجاج */
    html, body, [class*="css"], [data-testid="stAppViewContainer"] {
        font-family: 'Tajawal', sans-serif !important;
        direction: rtl;
        text-align: right;
        background: linear-gradient(135deg, #dbeafe 0%, #eff6ff 50%, #e0e7ff 100%) !important;
        background-attachment: fixed !important;
        animation: fadeIn 0.8s ease-in-out;
    }

    /* إخفاء شريط الهيدر العلوي الافتراضي */
    [data-testid="stHeader"] {
        background: transparent !important;
    }

    .stTextInput, .stSelectbox, .stTextArea, .stButton, .stDownloadButton {
        direction: rtl;
        text-align: right;
    }

    /* بطاقات الإحصائيات الزجاجية */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.55) !important;
        backdrop-filter: blur(14px) !important;
        -webkit-backdrop-filter: blur(14px) !important;
        padding: 16px !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.75) !important;
        border-right: 5px solid #1d63b8 !important;
        box-shadow: 0 8px 24px rgba(31, 38, 135, 0.06) !important;
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        background: rgba(255, 255, 255, 0.75) !important;
        box-shadow: 0 12px 28px rgba(31, 38, 135, 0.12) !important;
    }

    /* الترويسة الرسمية الزجاجية */
    .official-header {
        background: linear-gradient(135deg, rgba(13, 59, 102, 0.88) 0%, rgba(29, 99, 184, 0.84) 100%);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        padding: 25px;
        border-radius: 18px;
        text-align: center;
        color: white;
        margin-bottom: 25px;
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
    .official-header .emblem-badge:hover {
        transform: scale(1.1) rotate(5deg);
    }
    .official-header h1 {
        margin: 0;
        font-size: 22px;
        font-weight: 800;
        color: #ffffff;
    }
    .official-header p {
        margin: 8px 0 0 0;
        font-size: 15px;
        color: #f1f1f1;
        letter-spacing: 0.5px;
    }

    /* شريط تنبيه التاريخ والوقت الزجاجي */
    [data-testid="stAlert"] {
        background: rgba(255, 255, 255, 0.58) !important;
        backdrop-filter: blur(14px) !important;
        -webkit-backdrop-filter: blur(14px) !important;
        border: 1px solid rgba(255, 255, 255, 0.75) !important;
        border-right: 5px solid #1d63b8 !important;
        border-radius: 14px !important;
        box-shadow: 0 6px 20px rgba(31, 38, 135, 0.05) !important;
        color: #0f172a !important;
    }

    /* نموذج الإدخال الزجاجي */
    [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.6) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        padding: 25px !important;
        border-radius: 18px !important;
        border: 1px solid rgba(255, 255, 255, 0.8) !important;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.07) !important;
    }

    /* حقول الإدخال ومربع السجل الزجاجي */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.72) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.9) !important;
        transition: all 0.3s ease;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-color: #1d63b8 !important;
        box-shadow: 0 0 0 3px rgba(29, 99, 184, 0.15) !important;
    }

    /* الأزرار الزجاجية اللامعة */
    .stButton > button, .stFormSubmitButton > button, .stDownloadButton > button {
        background: linear-gradient(135deg, rgba(13, 59, 102, 0.92) 0%, rgba(29, 99, 184, 0.92) 100%) !important;
        backdrop-filter: blur(8px) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 12px !important;
        padding: 10px 22px !important;
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

# حساب الإحصائيات من الملف إن وجد
violations_count = 0
reinforcements_count = 0
data = ""

if os.path.exists("R.txt"):
    with open("R.txt", "r", encoding="utf-8") as f:
        data = f.read()
        for line in data.splitlines():
            if line.startswith("النوع: مخالفة"):
                violations_count += 1
            elif line.startswith("النوع: تعزيز"):
                reinforcements_count += 1

total_records = violations_count + reinforcements_count

# عرض الإحصائيات السريعة في 3 أعمدة زجاجية
col1, col2, col3 = st.columns(3)
col1.metric(label="📊 إجمالي السجلات", value=total_records)
col2.metric(label="🌟 التعزيزات", value=reinforcements_count)
col3.metric(label="⚠️ المخالفات", value=violations_count)

st.write("")

# جلب التاريخ والوقت الحالي بتوقيت سلطنة عمان
now = datetime.now(ZoneInfo("Asia/Muscat"))
current_date = now.strftime("%Y-%m-%d")
current_time = now.strftime("%H:%M:%S")

st.info(f"📅 التاريخ الحالي: {current_date} | ⏰ الساعة الحالية: {current_time}")

# نموذج إدخال البيانات
with st.form("data_form", clear_on_submit=True):
    id_val = st.text_input("معرف الطالب (ID)")
    type_val = st.selectbox("نوع السجل", ["مخالفة", "تعزيز"])
    details_val = st.text_input("التفاصيل (سبب المخالفة أو نوع التعزيز)")
    class_val = st.text_input("الفصل (Class)")

    submit_button = st.form_submit_button(label="إضافة وحفظ")

if submit_button:
    if id_val.strip() and details_val.strip() and class_val.strip():
        entry = f"النوع: {type_val} | المعرف: {id_val} | التفاصيل: {details_val} | التاريخ: {current_date} | الساعة: {current_time} | الفصل: {class_val}\n"

        with open("R.txt", "a", encoding="utf-8") as f:
            f.write(entry)

        st.session_state.show_balloons = True
        st.rerun()
    else:
        st.warning("يرجى ملء جميع الحقول المطلوبة قبل الإضافة.")

st.divider()

st.subheader("سجل المخالفات والتعزيزات المحفوظة في الملف")

if data.strip():
    st.text_area("جميع السجلات السابقة", data, height=200)

    st.download_button(
        label="تحميل ملف السجلات (R.txt)",
        data=data,
        file_name="R.txt",
        mime="text/plain",
    )

    st.divider()

    st.subheader("إدارة السجل (للمسؤول فقط)")
    secret_code = st.text_input(
        "أدخل الكود السري لحذف جميع السجلات", type="password"
    )

    # قراءة الكود السري من إعدادات Secrets بأمان
    admin_password = st.secrets.get("ADMIN_PASSWORD", "2013")

    if st.button("حذف السجل بالكامل"):
        if secret_code == admin_password:
            os.remove("R.txt")
            st.success("تم حذف جميع السجلات السابقة بنجاح!")
            st.rerun()
        else:
            st.error("الكود السري غير صحيح!")
else:
    st.info("لا يوجد سجل مسجل حتى الآن، قم بإضافة أول بيان.")
