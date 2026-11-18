    # زر لحذف جميع السجلات دفعة واحدة
    if st.button(
        "🗑️ حذف كافة السجلات نهائياً",
        type="secondary",
        use_container_width=True,
    ):
      if os.path.exists("R.txt"):
        os.remove("R.txt")
        st.success("تم حذف جميع السجلات بنجاح!")
        st.rerun()
