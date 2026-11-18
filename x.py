
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
        background-color: #f9f9f9;
    }
    .stTextInput, .stSelectbox, .stTextArea, .stButton, .stDownloadButton {
        direction: rtl;
        text-align: right;
    }
    /* تصميم ترويسة الشعار برمجياً */
    .header-box {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .header-box h1 {
        margin: 0;
        font-size: 24px;
        font-weight: bold;
    }
    .header-box p {
        margin: 5px 0 0 0;
        font-size: 16px;
        color: #e0e0e0;
    }
    </style>
    
    <!-- ترويسة مصممة برمجياً بالكامل -->
    <div class="header-box">
        <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-bottom: 5px;">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path>
        </svg>
        <h1>نظام سجل المخالفات والتعزيزات المدرسية</h1>
        <p>سلطنة عمان - وزارة التربية والتعليم[span_0](start_span)[span_0](end_span)</p>
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



