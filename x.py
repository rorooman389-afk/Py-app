import streamlit as st
import os

st.title("نظام سجل المخالفات والتعزيزات المدرسية")

# نموذج إدخال البيانات
with st.form("data_form"):
    id_val = st.text_input("معرف الطالب (ID)")
    type_val = st.selectbox("نوع السجل", ["مخالفة", "تعزيز"])
    details_val = st.text_input("التفاصيل (سبب المخالفة أو نوع التعزيز)")
    date_val = st.text_input("التاريخ")
    time_val = st.text_input("الساعة")
    class_val = st.text_input("الفصل (Class)")
    
    # زر داخل النموذج لحفظ البيانات وإضافتها للملف
    submit_button = st.form_submit_button(label="إضافة وحفظ")

if submit_button:
    if id_val and details_val and date_val and time_val and class_val:
        # تنسيق السطر المراد حفظه ليشمل نوع السجل والتفاصيل
        entry = f"النوع: {type_val} | المعرف: {id_val} | التفاصيل: {details_val} | التاريخ: {date_val} | الساعة: {time_val} | الفصل: {class_val}\n"
        
        # حفظ البيانات في ملف R.txt
        with open("R.txt", "a", encoding="utf-8") as f:
            f.write(entry)
            
        st.success("تمت إضافة وحفظ البيانات بنجاح!")
    else:
        st.warning("يرجى ملء جميع الحقول قبل الإضافة.")

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
            
            # قسم حذف المسجلين سابقاً بكود سري 2013
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
