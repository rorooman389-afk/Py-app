from datetime import datetime, timezone, timedelta
import os
import streamlit as st

st.set_page_config(page_title="نظام السجل المدرسي", page_icon="🇴🇲", layout="centered")

if "show_balloons" not in st.session_state:
    st.session_state.show_balloons = False

if st.session_state.show_balloons:
    st.balloons()
    st.session_state.show_balloons = False

CSS_STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');

html, body, [class*="css"], [data-testid="stAppViewContainer"] {
    font-family: 'Tajawal', sans-serif !important;
    direction: rtl;
    text-align: right;
    background-color: #e8f0fe !important;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stHeader"] {background: transparent !important;}

.official-header {
    background: linear-gradient(135deg, #0d3b66 0%, #1d63b8 100%);
    padding: 25px;
    border-radius: 18px;
    text-align: center;
    color: white;
    margin-bottom: 22px;
    border-bottom: 4px solid #d4af37;
}

.official-header .emblem-badge {
    font-size: 32px;
    background: rgba(255, 255, 255, 0.15);
    width: 68px;
    height: 68px;
    line-height: 68px;
    border-radius: 50%;
    margin: 0 auto 12px auto;
    display: block;
    border: 1.5px solid rgba(212, 175, 55, 0.65);
}

.glass-record-card {
    background: rgba(255, 255, 255, 0.8);
    padding: 15px 20px;
    border-radius: 15px;
    margin-bottom: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}
.border-positive {border-right: 5px solid #10b981;}
.border-negative {border-right: 5px solid #ef4444;}
.border-neutral {border-right: 5px solid #1d63b8;}

.pill-positive {
    background: #d1fae5;
    color: #065f46;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 700;
}
.pill-negative {
    background: #fee2e2;
    color: #991b1b;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 700;
}
</style>

<div class="official-header">
    <span class="emblem-badge">🇴🇲</span>
    <h1>سلطنة عمان - وزارة التربية والتعليم</h1>
    <p>نظام سجل المخالفات والتعزيزات المدرسية</p>
</div>
"""

st.markdown(CSS_STYLE, unsafe_allow_html=True)


def render_card(line_text):
    try:
        parts = [p.strip() for p in line_text.split("|")]
        if len(parts) >= 6:
            r_type = parts[0].replace("النوع:", "").strip()
            r_id = parts[1].replace("المعرف:", "").strip()
            r_details = parts[2].replace("التفاصيل:", "").strip()
            r_date = parts[3].replace("التاريخ:", "").strip()
            r_time = parts[4].replace("الساعة:", "").strip()
            r_class = parts[5].replace("الفصل:", "").strip()

            is_pos = r_type == "تعزيز"
            b_cls = "border-positive" if is_pos else "border-negative"
            p_cls = "pill-positive" if is_pos else "pill-negative"
            icon = "🌟" if is_pos else "⚠️"

            html = f"""
            <div class="glass-record-card {b_cls}">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span class="{p_cls}">{icon} {r_type}</span>
                    <span style="color: #475569; font-size: 13px;">📅 {r_date} | ⏰ {r_time}</span>
                </div>
                <div style="font-size: 16px; font-weight: 700; color: #0f172a; margin-bottom: 4px;">
                    معرف الطالب: {r_id} &nbsp;•&nbsp; الفصل: {r_class}
                </div>
                <div style="color: #334155; font-size: 15px;">{r_details}</div>
            </div>
            """
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div class="glass-record-card border-neutral">{line_text}</div>',
                unsafe_allow_html=True,
            )
    except Exception:
        st.markdown(
            f'<div class="glass-record-card border-neutral">{line_text}</div>',
            unsafe_allow_html=True,
        )


violations_count = 0
reinforcements_count = 0
data = ""

if os.path.exists("R.txt"):
    with open("R.txt", "r", encoding="utf-8") as f:
        data = f.read()
    for line in data.splitlines():
        if "النوع: مخالفة" in line:
            violations_count += 1
        elif "النوع: تعزيز" in line:
            reinforcements_count += 1

total_records = violations_count + reinforcements_count

col1, col2, col3 = st.columns(3)
col1.metric(label="📊 إجمالي السجلات", value=total_records)
col2.metric(label="🌟 التعزيزات", value=reinforcements_count)
col3.metric(label="⚠️ المخالفات", value=violations_count)

st.write("")

oman_tz = timezone(timedelta(hours=4))
now = datetime.now(oman_tz)
current_date = now.strftime("%Y-%m-%d")
current_time = now.strftime("%H:%M:%S")

st.info(f"📅 التاريخ الحالي: {current_date} | ⏰ الساعة الحالية: {current_time}")

with st.form("data_form", clear_on_submit=True):
    st.markdown("#### 📝 تسجيل بيان جديد")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        record_type = st.selectbox("نوع السجل", ["تعزيز", "مخالفة"], index=0)
    with col_f2:
        student_id = st.text_input("معرف الطالب / الرقم المدني", placeholder="أدخل رقم الطالب...")

    class_name = st.selectbox(
        "الصف / الفصل الدراسي",
        ["خامس أ", "خامس ب", "سادس أ", "سادس ب", "سابع أ", "سابع ب"],
    )

    details = st.text_area("التفاصيل / السبب", placeholder="اكتب تفاصيل المخالفة أو التعزيز هنا...")

    submit_button = st.form_submit_button(label="حفظ السجل")

    if submit_button:
        if not student_id.strip() or not details.strip():
            st.error("الرجاء تعبئة جميع الحقول المطلوبة (معرف الطالب والتفاصيل).")
        else:
            try:
                new_line = f"النوع: {record_type} | المعرف: {student_id.strip()} | التفاصيل: {details.strip()} | التاريخ: {current_date} | الساعة: {current_time} | الفصل: {class_name}"

                with open("R.txt", "a", encoding="utf-8") as f:
                    f.write(new_line + "\n")

                st.session_state.show_balloons = True
                st.success("تم حفظ السجل بنجاح!")
                st.rerun()
            except Exception as e:
                st.error(f"حدث خطأ أثناء الحفظ: {e}")

st.markdown("---")
st.markdown("### 📋 سجلات النظام")

if data.strip():
    search_query = st.text_input("🔍 ابحث في السجلات (برقم الطالب أو الفصل):", placeholder="ابحث هنا...")

    lines = [line.strip() for line in data.splitlines() if line.strip()]
    lines.reverse()

    if search_query:
        lines = [l for l in lines if search_query in l or search_query.lower() in l.lower()]
        st.write(f"نتائج البحث عن: **{search_query}** ({len(lines)} نتيجة)")

    if lines:
        for line in lines:
            render
