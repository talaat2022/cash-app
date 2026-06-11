
import streamlit as st
import requests

# 1. إعدادات واجهة التطبيق
st.set_page_config(page_title="Cash App", page_icon="📱", layout="centered")

st.title("📱 تطبيق كاش آب للخدمات")
st.subheader("شحن كروت فكة ومارد - فودافون")
st.write("---")

FAKKA_PRODUCTS = [("فكة  2.5  جنيه", "Fakka_2.5_Unite"), ("فكة  4.25 جنيه", "Fakka_4.25_Unite"), ("فكة  5    جنيه", "Fakka_5_Unite")]
receiver = st.text_input("📱 أدخل الرقم المراد الشحن له (11 رقم):", placeholder="01xxxxxxxxx")
pin = st.text_input("🔒 أدخل الرقم السري للمحفظة:", type="password", placeholder="******")

if st.button("🚀 ابدأ عملية الشحن الآن", use_container_width=True):
    if not (receiver.startswith("01") and len(receiver) == 11) or not pin:
        st.error("❌ تأكد من البيانات المرسلة")
    else:
        with st.spinner("جاري فحص اتصال السيرفر بـ فودافون..."):
            try:
                url_seamless = "http://mobile.vodafone.com.eg/checkSeamless/realms/vf-realm/protocol/openid-connect/auth?client_id=ana-vodafone-app-seamless"
                headers_seamless = {
                    'User-Agent': "okhttp/4.11.0",
                    'Connection': "Keep-Alive",
                    'Accept-Encoding': "gzip",
                    'x-agent-operatingsystem': "13",
                    'clientId': "AnaVodafoneAndroid",
                    'Accept-Language': "ar",
                    'x-agent-device': "OPPO CPH2235",
                    'x-agent-version': "2024.7.2.1",
                    'x-agent-build': "1050",
                    'digitalId': "24S0M31T0I9RK"
                }

                response_seamless = requests.get(url_seamless, headers=headers_seamless, timeout=15)
                
                # 🟢 إظهار النتيجة فوراً أياً كانت على الشاشة لموقعك
                st.warning(f"⚠️ استجابة الخادم: كود {response_seamless.status_code}")
                
                # صندوق لعرض الرد الخام لو كان نص أو خطأ حماية
                st.info("🔍 الرد التفصيلي الصادر من فودافون:")
                st.text_area("نص الاستجابة الحالي:", value=response_seamless.text, height=250)
                
                try:
                    seamless_data = response_seamless.json()
                    st.success("✅ السيرفر رد بـ JSON صالحة!")
                except:
                    st.error("❌ الرد الحالي ليس JSON. فودافون ترفض تمرير التوكن.")

            except Exception as e:
                st.error(f"❌ خطأ اتصال: {e}")
                
