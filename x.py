import streamlit as st
import os
from datetime import datetime

# شريط جانب اختيار اللغة
lang = st.sidebar.selectbox("اختر اللغة / Select Language", ["العربية", "English"])

# تحديد النصوص بناءً على اللغة المختارة
if lang == "العربية":
    ministry_title = "سلطنة عمان - وزارة التربية والتعليم"
    system_title = "نظام سجل المخالفات والتعزيزات المدرسية"
    date_label = "📅 التاريخ الحالي"
    time_label = "⏰ الساعة الحالية"
    id_input = "معرف الطالب (ID)"
    type_input = "نوع السجل"
    opt_1 = "مخالفة"
    opt_2 = "تعزيز"
    details_input = "التفاصيل (سبب المخالفة أو نوع التعزيز)"
    class_input = "الفصل (Class)"
    submit_btn = "إضافة وحفظ"
    success_save = "تمت إضافة وحفظ البيانات بنجاح!"
    warning_fill = "يرجى ملء جميع الحقول المطلوبة قبل الإضافة."
    history_header = "سجل المخالفات والتعزيزات المحفوظة في الملف"
    area_label = "جميع السجلات السابقة"
    download_btn_label = "تحميل ملف السجلات (R.txt)"
    admin_header = "إدارة السجل (للمسؤول فقط)"
    secret_prompt = "أدخل الكود السري لحذف جميع السجلات"
    delete_btn_label = "حذف السجل بالكامل"
    delete_success = "تم حذف جميع السجلات السابقة بنجاح!"
    delete_error = "الكود السري غير صحيح!"
    file_empty = "الملف فارغ حالياً."
    no_file = "لا يوجد سجل مسجل حتى الآن، قم بإضافة أول بيان."
    dir_val = "rtl"
    align_val = "right"
else:
    ministry_title = "Sultanate of Oman - Ministry of Education"
    system_title = "School Violations and Reinforcements Record System"
    date_label = "📅 Current Date"
    time_label = "⏰ Current Time"
    id_input = "Student ID"
    type_input = "Record Type"
    opt_1 = "Violation"
    opt_2 = "Reinforcement"
    details_input = "Details (Reason or Reinforcement Type)"
    class_input = "Class"
    submit_btn = "Add and Save"
    success_save = "Data added and saved successfully!"
    warning_fill = "Please fill in all required fields."
    history_header = "Saved Violations and Reinforcements Records"
    area_label = "All Previous Records"
    download_btn_label = "Download Records File (R.txt)"
    admin_header = "Record Management (Admin Only)"
    secret_prompt = "Enter Secret Code to Delete All Records"
    delete_btn_label = "Delete All Records"
    delete_success = "All previous records deleted successfully!"
    delete_error = "Incorrect secret code!"
    file_empty = "The file is currently empty."
    no_file = "No records found yet, add your first entry."
    dir_val = "ltr"
    align_val = "left"

# إعداد واجهة الصفحة وتنسيق الاتجاه حسب اللغة
st.markdown(
    f"""
    <style>
    body, [data-testid="stAppViewContainer"] {{
        direction: {dir_val};
        text-align: {align_val};
        background-color: #f8f9fa;
    }}
    .stTextInput, .stSelectbox, .stTextArea, .stButton, .stDownloadButton {{
        direction: rtl;
        text-align: right;
    }}
    .official-header {{
        background: linear-gradient(135deg, #0d3b66 0%, #1d63b8 100%);
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-bottom: 4px solid #d4af37;
    }}
    .official-header .emblem-badge {{
        font-size: 32px;
        background: rgba(255, 255, 255, 0.15);
        width: 65px;
        height: 65px;
        line-height: 65px;
        border-radius: 50%;
        margin: 0 auto 12px auto;
        display: block;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }}
    .official-header h1 {{
        margin: 0;
        font-size: 22px;
        font-weight: bold;
        color: #ffffff;
    }}
    .official-header p {{
        margin: 8px 0 0 0;
        font-size: 15px;
        color: #f1f1f1;
        letter-spacing: 0.5px;
    }}
    </style>
    
    <div class="official-header">
        <span class="emblem-badge">🇴🇲</span>
        <h1>{ministry_title}</h1>
        <p>{system_title}</p>
    </div>
    """,
    unsafe_allow_html=True
)

# جلب التاريخ والوقت الحالي تلقائياً
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")
current_time = now.strftime("%H:%M:%S")

st.info(f"{date_label}: {current_date} | {time_label}: {current_time}")

# نموذج إدخال البيانات
with st.form("data_form"):
    id_val = st.text_input(id_input)
    type_val = st.selectbox(type_input, [opt_1, opt_2])
    details_val = st.text_input(details_input)
    class_val = st.text_input(class_input)
    
    submit_button = st.form_submit_button(label=submit_btn)

if submit_button:
    if id_val and details_val and class_val:
        entry = f"النوع: {type_val} | المعرف: {id_val} | التفاصيل: {details_val} | التاريخ: {current_date} | الساعة: {current_time} | الفصل: {class_val}\n"
        
        with open("R.txt", "a", encoding="utf-8") as f:
            f.write(entry)
            
        st.success(success_save)
        st.rerun()
    else:
        st.warning(warning_fill)

st.divider()

st.subheader(history_header)

if os.path.exists("R.txt"):
    with open("R.txt", "r", encoding="utf-8") as f:
        data = f.read()
        
    if data.strip():
        st.text_area(area_label, data, height=200)
        
        st.download_button(
            label=download_btn_label,
            data=data,
            file_name="R.txt",
            mime="text/plain"
        )
        
        st.divider()
        
        st.subheader(admin_header)
        secret_code = st.text_input(secret_prompt, type="password")
        if st.button(delete_btn_label):
            if secret_code == "2013":
                os.remove("R.txt")
                st.success(delete_success)
                st.rerun()
            else:
                st.error(delete_error)
    else:
        st.info(file_empty)
else:
    st.info(no_file)
