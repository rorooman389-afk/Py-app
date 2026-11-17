import streamlit as st
import os

st.title("نظام إدخال وتخزين البيانات المتعددة")

# نموذج إدخال البيانات
with st.form("data_form"):
    id_val = st.text_input("المعرف (ID)")
    date_val = st.text_input("التاريخ")
    time_val = st.text_input("الساعة")  # تمت إضافة حقل الساعة هنا
    class_val = st.text_input("الفصل (Class)")
    
    # زر داخل النموذج لحفظ البيانات وإضافتها للملف
    submit_button = st.form_submit_button(label="إضافة وحفظ")

if submit_button:
    if id_val and date_val and time_val and class_val:
        # تنسيق السطر المراد حفظه مع الساعة
        entry = f"المعرف: {id_val} | التاريخ: {date_val} | الساعة: {time_val} | الفصل: {class_val}\n"
        
        # حفظ البيانات في ملف R.txt (بوضع a+ لإضافة البيانات الجديدة دون مسح القديمة)
        with open("R.txt", "a", encoding="utf-8") as f:
            f.write(entry)
            
        st.success("تمت إضافة وحفظ البيانات بنجاح!")
    else:
        st.warning("يرجى ملء جميع الحقول قبل الإضافة.")

st.divider()

# عرض محتوى ملف R.txt بالكامل (جميع المعرفات والبيانات المخزنة)
st.subheader("سجل البيانات المحفوظة في الملف")
if os.path.exists("R.txt"):
    with open("السجل.txt", "r", encoding="utf-8") as f:
        data = f.read()
        if data.strip():
            st.text_area("جميع المدخلات السابقة", data, height=200)
            
            # زر لتحميل الملف بصيغة txt مباشرة من المتصفح
            st.download_button(
                label="تحميل ملف البيانات (R.txt)",
                data=data,
                file_name="R.txt",
                mime="text/plain"
            )
            
            st.divider()
            
            # قسم حذف المسجلين سابقاً بكود سري
            st.subheader("إدارة السجل (للمسؤول فقط)")
            secret_code = st.text_input("أدخل الكود السري لحذف جميع المسجلين", type="password")
            if st.button("حذف السجل بالكامل"):
                if secret_code == "1234":  # يمكنك تغيير 1234 إلى الكود السري الذي تريده
                    os.remove("R.txt")
                    st.success("تم حذف جميع البيانات السابقة بنجاح!")
                    st.rerun()
                else:
                    st.error("الكود السري غير صحيح!")
        else:
            st.info("الملف فارغ حالياً.")
else:
    st.info("لا يوجد ملف مسجل حتى الآن، قم بإضافة أول بيان.")
