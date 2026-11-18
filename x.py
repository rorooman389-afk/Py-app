from datetime import datetime, timedelta, timezone
import os
import streamlit as st

st.set_page_config(page_title="نظام السجل المدرسي", page_icon="🇴🇲", layout="centered")

if "show_balloons" not in st.session_state:
    st.session_state.show_balloons = False

if st.session_state.show_balloons:
    st.balloons()
    st.session_state.show_balloons = False

st.markdown(
    "<style>"
    "@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');"
    "html, body, [class*='css'], [data-testid='stAppViewContainer'] {"
    "font-family: 'Tajawal', sans-serif !important;"
    "direction: rtl; text-align: right; background-color: #e8f0fe !important;"
    "}"
    "#MainMenu, footer {visibility: hidden;}"
    "[data-testid='stHeader'] {background: transparent !important;}"
    ".official-header {"
    "background: linear-gradient(135deg, #0d3b66 0%, #1d63b8 100%);"
    "padding: 25px; border-radius: 18px; text-align: center; color: white;"
    "margin-bottom: 22px; border-bottom: 4px solid #d4af37;"
    "}"
    ".official-header .emblem-badge {"
    "font-size: 32px; background: rgba(255, 255, 255, 0.15);"
    "width: 68px; height: 68px; line-height: 68px; border-radius: 50%;"
    "margin: 0 auto 12px auto; display: block;"
    "border: 1.5px solid rgba(212, 175, 55, 0.65);"
    "}"
    ".glass-record-card {"
    "background: rgba(255, 255, 255, 0.8); padding: 15px 20px;"
    "border-radius: 15px; margin-bottom: 12px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);"
    "}"
    ".border-positive {border-right: 5px solid #10b981;}"
    ".border-negative {border-right: 5px solid #ef4444;}"
    ".border-neutral {border-right: 5px solid #1d63b8;}"
    ".pill-positive {background: #d1fae5; color: #065f46; padding: 3px 12px; border-radius: 20px; font-size: 13px; font-weight: 700;}"
    ".pill-negative {background: #fee2e2; color: #991b1b; padding: 3px 12px; border-radius: 20px; font-size: 13px; font-weight: 700;}"
    "</style>"
    "<div class='official-header'>"
    "<span class='emblem-badge'>🇴🇲</span>"
    "<h1>سلطنة عمان - وزارة التربية والتعليم</h1>"
    "<p>نظام سجل المخالفات والتعزيزات المدرسية</p>"
    "</div>",
    unsafe_allow_html=True,
)


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

      card_html = (
          "<div class='
