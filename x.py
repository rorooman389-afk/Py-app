import streamlit as st
import os
from datetime import datetime

# إعداد الصفحة لتكون المحاذاة من اليمين ليسار ودعم اللغة العربية
st.markdown(
    """
    <style>
    body, [data-testid="stAppViewContainer"] {
        direction: rtl;
        text-align: right;
    }
    .stTextInput, .stSelectbox, .stTextArea, .stButton, .stDownloadButton {
        direction: rtl;
        text-align: right;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("نظام سجل المخالفات والتعزيزات المدرسية")

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
    
    # زر داخل النموذج لحفظ البيانات وإضافتها للملف
    submit_button = st.form_submit_button(label="إضافة وحفظ")

if submit_button:
    if id_val and details_val and class_val:
        # تنسيق السطر المراد حفظه مع إدراج التاريخ والوقت التلقائي
        entry = f"النوع: {type_val} | المعرف: {id_val} | التفاصيل: {details_val} | التاريخ: {current_date} | الساعة: {current_time} | الفصل: {class_val}\n"
        
        # حفظ البيانات في ملف R.txt
        with open("R.txt", "a", encoding="utf-8") as f:
            f.write(entry)
            
        st.success("تمت إضافة وحفظ البيانات بنجاح!")
        st.rerun()
    else:
        st.warning("يرجى ملء جميع الحقول المطلوبة قبل الإضافة.")

st.divider()

# عرض محتوى ملف R.txt بالكامل
st.subheader("سجل المخالفات والتعزيزات المحفوظة في الملف")

if os.path.exists("R.txt"):
    with open("R.txt", "r", encoding="utf-8") as f:
        data = f.read()
        
    if data.strip():
        st.text_area("جميع السجلات السابقة", data, height=200)
        
        # زر لتحميل الملف بصيغة txt مباشرة من المتصفح
        st.download_button(
            label="تحميل ملف السجلات (R.txt)",
            data=data,
            file_name="R.txt",
            mime="text/plain"
        )
        
        st.divider()
        
        # قسم حذف السجل بكود سري 2013
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


