"import streamlit as st
import requests
import json

# 1. إعدادات واجهة التطبيق (الوجه المرئي)
st.set_page_config(page_title="Cash App", page_icon="📱", layout="centered")

st.title("📱 تطبيق كاش آب للخدمات")
st.subheader("شحن كروت فكة ومارد - فودافون")
st.write("---")

FAKKA_PRODUCTS = [
    ("فكة  2.5  جنيه", "Fakka_2.5_Unite"),
    ("فكة  4.25 جنيه", "Fakka_4.25_Unite"),
    ("فكة  5    جنيه", "Fakka_5_Unite"),
    ("فكة  6    جنيه", "Fakka_6_NewUnite"),
    ("فكة  7    جنيه", "Fakka_7_Unite"),
    ("فكة  9    جنيه", "Fakka_9_Unite"),
    ("فكة  10   جنيه", "Fakka_10_Unite"),
    ("فكة  10   جنيه (new)", "Fakka_10_NewUnite"),
    ("فكة  10.5 جنيه", "Fakka_10.5_Unite"),
    ("فكة  11.5 جنيه", "Fakka_11.5_Unite"),
    ("فكة  12   جنيه", "Fakka_12_Unite"),
    ("فكة  12.5 جنيه", "Fakka_12.5_Unite"),
    ("فكة  13   جنيه", "Fakka_13_Unite"),
    ("فكة  13.5 جنيه", "Fakka_13.5_Unite"),
    ("فكة  15   جنيه", "Fakka_15_Unite"),
    ("فكة  15   جنيه (new)", "Fakka_15_NewUnite"),
    ("فكة  15.5 جنيه", "Fakka_15.5_Unite"),
    ("فكة  16.5 جنيه", "Fakka_16.5_Unite"),
    ("فكة  17.5 جنيه", "Fakka_17.5_Unite"),
    ("فكة  19.5 جنيه", "Fakka_19.5_NewUnite"),
    ("فكة  20   جنيه", "Fakka_20_Unite"),
    ("فكة  26   جنيه", "Fakka_26_Unite"),
]

MARED_PRODUCTS = [
    ("مارد 10 دقايق", "Mared_10_Minuts"),
    ("مارد 10 فليكس", "Mared_10_Flexs"),
    ("مارد 10 سوشيال", "Mared_10_Social"),
]

ALL_PRODUCTS = FAKKA_PRODUCTS + MARED_PRODUCTS

# أزرار وقوائم واجهة المستخدم المروية
product_names = [item[0] for item in ALL_PRODUCTS]
selected_name = st.selectbox("📋 اختر الكرت المطلوب من القائمة:", product_names)

product_id = ""
for name, pid in ALL_PRODUCTS:
    if name == selected_name:
        product_id = pid
        break

receiver = st.text_input("📱 أدخل الرقم المراد الشحن له (11 رقم):", placeholder="01xxxxxxxxx")
pin = st.text_input("🔒 أدخل الرقم السري للمحفظة:", type="password", placeholder="******")

# 2. أوامر التشغيل والربط الفعلي بالخادم (السكريبت الأساسي)
if st.button("🚀 ابدأ عملية الشحن الآن", use_container_width=True):
    if not (receiver.startswith("01") and len(receiver) == 11):
        st.error("❌ عذراً، رقم الهاتف غير صحيح!")
    elif not pin:
        st.error("❌ يرجى إدخال الرقم السري للمحفظة.")
    else:
        with st.spinner("جاري الاتصال بالسيرفر وتثبيت العملية الفعلية..."):
"
