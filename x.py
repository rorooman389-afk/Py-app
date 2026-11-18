import streamlit as str_module
import os
from datetime import datetime

# إعداد الصفحة لتكون المحاذاة من اليمين ليسار ودعم اللغة العربية
str_module.markdown(
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

# وضع شعار وزارة التربية والتعليم في سلطنة عمان في أعلى الواجهة
str_module.image("https://upload.wikimedia.org/wikipedia/commons/2/2f/Emblem_of_Oman.svg", width=120)
str_module.title("نظام سجل المخالفات والتعزيزات المدرسية")
str_module.subheader("سلطنة عمان - وزارة التربية والتعليم")[span_1](start_span)[span_1](end_span)

# جلب التاريخ والوقت الحالي تلقائياً
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")
current_time = now.strftime("%H:%M:%S")

str_module.info(f"📅 التاريخ الحالي: {current_date} | ⏰ الساعة الحالية: {current_time}")

# نموذج إدخال البيانات
with str_module.form("data_form"):
    id_val = str_module.text_input("معرف الطالب (ID)")
    type_val = str_module.selectbox("نوع السجل", ["مخالفة", "تعزيز"])
    details_val = str_module.text_input("التفاصيل (سبب المخالفة أو نوع التعزيز)")
    class_val = str_module.text_input("الفصل (Class)")
    
    # زر داخل النموذج لحفظ البيانات وإضافتها للملف
    submit_button = str_module.form_submit_button(label="إضافة وحفظ")

if submit_button:
    if id_val and details_val and class_val:
        # تنسيق السطر المراد حفظه مع إدراج التاريخ والوقت التلقائي
        entry = f"النوع: {type_val} | المعرف: {id_val} | التفاصيل: {details_val} | التاريخ: {current_date} | الساعة: {current_time} | الفصل: {class_val}\n"
        
        # حفظ البيانات في ملف R.txt
        with open("R.txt", "a", encoding="utf-8") as f:
            f.write(entry)
            
        str_module.success("تمت إضافة وحفظ البيانات بنجاح!")
        str_module.rerun()
    else:
        str_module.warning("يرجى ملء جميع الحقول المطلوبة قبل الإضافة.")

str_module.divider()

# عرض محتوى ملف R.txt بالكامل
str_module.subheader("سجل المخالفات والتعزيزات المحفوظة في الملف")

if os.path.exists("R.txt"):
    with open("R.txt", "r", encoding="utf-8") as f:
        data = f.read()
        
    if data.strip():
        str_module.text_area("جميع السجلات السابقة", data, height=200)
        
        # زر لتحميل الملف بصيغة txt مباشرة من المتصفح
        str_module.download_button(
            label="تحميل ملف السجلات (R.txt)",
            data=data,
            file_name="R.txt",
            mime="text/plain"
        )
        
        str_module.divider()
        
        # قسم حذف السجل بكود سري 2013
        str_module.subheader("إدارة السجل (للمسؤول فقط)")
        secret_code = str_module.text_input("أدخل الكود السري لحذف جميع السجلات", type="password")
        if str_module.button("حذف السجل بالكامل"):
            if secret_code == "2013":
                os.remove("R.txt")
                str_module.success("تم حذف جميع السجلات السابقة بنجاح!")
                str_module.rerun()
            else:
                str_module.error("الكود السري غير صحيح!")
    else:
        str_module.info("الملف فارغ حالياً.")
else:
    str_module.info("لا يوجد سجل مسجل حتى الآن، قم بإضافة أول بيان.")



