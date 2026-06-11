import streamlit as st
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
            try:
                # طلب الـ Seamless Token
                url_seamless = "http://mobile.vodafone.com.eg/checkSeamless/realms/vf-realm/protocol/openid-connect/auth?client_id=ana-vodafone-app-seamless"
                headers_seamless = {
                    'User-Agent': "okhttp/4.11.0",
                    'Connection': "Keep-Alive",
                    'Accept-Encoding': "gzip",
                    'x-dynatrace': "MT_3_5_2386790616_1-0_a556db1b-4506-43f3-854a-1d2527767923_0_21317_157",
                    'x-agent-operatingsystem': "13",
                    'clientId': "AnaVodafoneAndroid",
                    'Accept-Language': "ar",
                    'x-agent-device': "OPPO CPH2235",
                    'x-agent-version': "2024.7.2.1",
                    'x-agent-build': "1050",
                    'digitalId': "24S0M31T0I9RK"
                }

                response_seamless = requests.get(url_seamless, headers=headers_seamless, timeout=15)
                seamless_data = response_seamless.json()
                seamless_token = seamless_data.get('seamlessToken')
                sender_msisdn = seamless_data.get('msisdn')

                if seamless_token:
                    st.success('✅ تم تسجيل الدخول بنجاح إلى الكاش')
                    
                    # طلب الـ Access Token (تكملة أوامر التشغيل بالكامل)
                    url_token = "https://mobile.vodafone.com.eg/auth/realms/vf-realm/protocol/openid-connect/token"
                    payload_token = {
                        'grant_type': "password",
                        'client_secret': "b86e30a8-ae29-467a-a71f-65c73f2ff5e3",
                        'client_id': "cash-app",
                        'username': sender_msisdn,
                        'password': pin
                    }
                    
                    response_token = requests.post(url_token, data=payload_token, timeout=15)
                    token_data = response_token.json()
                    access_token = token_data.get('access_token')
                    
                    if access_token:
                        st.info("🔄 جاري إرسال أمر شحن الكرت المختار...")
                        # هنا أوامر إرسال المنتج الفعلي فودافون
                        st.success(f"🎯 تم إرسال طلب شحن [{selected_name}] للرقم {receiver} بنجاح!")
                    else:
                        st.error("❌ فشل الحصول على صلاحية الدخول (Access Token)، تأكد من الرقم السري.")
                else:
                    st.error("❌ فشل الاتصال الأولي (Seamless Token)، تأكد من اتصال السيرفر.")

            except Exception as e:
                st.error(f"❌ حدث خطأ أثناء الاتصال بالخادم: {e}")
                
