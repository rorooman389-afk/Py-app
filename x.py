import streamlit as st
import os
from datetime import datetime

# إعداد الصفحة لتكون المحاذاة من اليمين ليسار ودعم اللغة العربية وتصميم الواجهة برمجياً
st.markdown(
    """
    <style>
    body, [data-testid="stAppViewContainer"] {
        direction: rtl;
        text-align: right;
        background-color: #f8f9fa;
    }
    .stTextInput, .stSelectbox, .stTextArea, .stButton, .stDownloadButton {
        direction: rtl;
        text-align: right;
    }
    /* تصميم ترويسة الشعار والوزارة برمجياً بالكامل */
    .official-header {
        background: linear-gradient(135deg, #0d3b66 0%, #1d63b8 100%);
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-bottom: 4px solid #d4af37;
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
    
    <!-- ترويسة رسمية مصممة برمجياً -->
    <div class="official-header">
        <span class="emblem-badge">🇴🇲</span>
        <h1>سلطنة عمان - وزارة التربية والتعليم</h1>
        <p>نظام سجل المخالفات والتعزيزات المدرسية</p>
    </div>
    """,
    unsafe_allow_html=True
)

# جلب التاريخ والوقت الحالي تلقائياً
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")
current_time = now.strftime("%H:%M:%S")

st.info(f"📅 التاريخ الحالي: {current_date} | ⏰ الساعة الحالية: {current_time}")

# نموذج إدخال البيانات
with st.form("data_form"):
    id_val = st.text_input("معرف الطالب (ID)")
    type_val = st.selectbox("نوع السجل", ["مخالفة", "تعزيز"])
    details_val = st.text_input("التفاصيل (سبب المخالفة أو نوع التعزيز)")
    class_val = st.text_input("الفصل (Class)")
    
    submit_button = st.form_submit_button(label="إضافة وحفظ")

if submit_button:
    if id_val and details_val and class_val:
        entry = f"النوع: {type_val} | المعرف: {id_val} | التفاصيل: {details_val} | التاريخ: {current_date} | الساعة: {current_time} | الفصل: {class_val}\n"
        
        with open("R.txt", "a", encoding="utf-8") as f:
            f.write(entry)
            
        st.success("تمت إضافة وحفظ البيانات بنجاح!")
        st.rerun()
    else:
        st.warning("يرجى ملء جميع الحقول المطلوبة قبل الإضافة.")

st.divider()

st.subheader("سجل المخالفات والتعزيزات المحفوظة في الملف")

if os.path.exists("R.txt"):
    with open("R.txt", "r", encoding="utf-8") as f:
        data = f.read()
        
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
        if st.button("حذف السجل بالكامل"):
            if secret_code == "2013":
                os.remove("R.txt")
                st.success("تم حذف جميع السجلات السابقة بنجاح!")
                st.rerun()
            else:
                st.error("الكود السري غير صحيح!")
    else:
        st.info("الملف فارغ حالياً.")
else:
    st.info("لا يوجد سجل مسجل حتى الآن، قم بإضافة أول بيان.")
