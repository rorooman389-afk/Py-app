import streamlit as st
import os

st.title("إدارة البيانات التفاعلية")

id_val = st.text_input("المعرف (ID)")
date_val = st.text_input("التاريخ")
class_val = st.text_input("الفصل (Class)")

if st.button("حفظ وعرض"):
    if id_val and date_val and class_val:
        entry = f"{id_val} - {date_val} - {class_val}\n"
        with open("R.txt", "a") as f:
            f.write(entry)
        st.success("تم الحفظ!")
    else:
        st.warning("يرجى ملء جميع الحقول.")

st.subheader("البيانات المحفوظة")
if os.path.exists("R.txt"):
    with open("R.txt", "r") as f:
        data = f.read()
        st.text_area("السجل الحالي", data, height=150)
else:
    st.info("لا توجد بيانات مسجلة بعد.")

