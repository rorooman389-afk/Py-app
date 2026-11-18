import streamlit as st
import os
from datetime import datetime
from zoneinfo import ZoneInfo

st.set_page_config(page_title="نظام السجل المدرسي", page_icon="🇴🇲", layout="centered")

# تهيئة حالة الجلسة لإظهار البالونات بعد إعادة تحميل الصفحة
if "show_balloons" not in st.session_state:
    st.session_state.show_balloons = False

if st.session_state.show_balloons:
    st.balloons()
    st.session_state.show_balloons = False

# تصميم الواجهة ودعم اللغة العربية وتنسيق بطاقات الإحصائيات
st.markdown(
    """
    <style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    body, [data-testid="stAppViewContainer"] {
        direction: rtl;
        text-align: right;
        background-color: #f8f9fa;
        animation: fadeIn 0.8s ease-in-out;
    }
    .stTextInput, .stSelectbox, .stTextArea, .stButton, .stDownloadButton {
        direction: rtl;
        text-align: right;
    }
    [data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border-right: 4px solid #1d63b8;
        text-align: center;
    }
    .official-header {
        background: linear-gradient(135deg, #0d3b66 0%, #1d63b8 100%);
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-bottom: 4px solid #d4af37;
        animation: fadeIn 1s ease-in-out;
    }
    .official-header .emblem-badge {
        font-size: 32px;
        background: rgba(255, 255, 255, 0.15);
        width: 65px;
        height: 65px;
        line-height: 65px;
        border-radius: 50%;
        margin: 0 auto 12px auto;
        display: block;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }
    .official-header .emblem-badge:hover {
        transform: scale(1.1);
    }
    .official-header h1 {
        margin: 0;
        font-size: 22px;
        font-weight: bold;
        color: #ffffff;
    }
    .official-header p {
        margin: 8px 0 0 0;
        font-size: 15px;
        color: #f1f1f1;
        letter-spacing: 0.5px;
    }
    </style>
    
    <div class="official-header">
        <span class="emblem-badge">🇴🇲</span>
        <h1>سلطنة عمان - وزارة التربية والتعليم</h1>
        <p>نظام سجل المخالفات والتعزيزات المدرسية</p>
    </div>
    """,
    unsafe_allow_html=True
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

# عرض الإحصائيات السريعة في 3 أعمدة
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
        mime="text/plain"
    )
    
    st.divider()
    
    st.subheader("إدارة السجل (للمسؤول فقط)")
    secret_code = st.text_input("أدخل الكود السري لحذف جميع السجلات", type="password")
    
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
