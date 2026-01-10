import streamlit as st
import requests
import random

# صفحے کی بنیادی سیٹنگ
st.set_page_config(page_title="YouTube One-Click Uploader", page_icon="🚀", layout="centered")

# ٹائٹل اور ڈیزائن
st.title("🎬 یوٹیوب ون کلک اپلوڈر")
st.markdown("---")

# پاور ورڈز کی لسٹ
power_words = ["AMAZING", "SHOCKING", "MUST WATCH", "UNBELIEVABLE", "SECRET", "EPIC"]

# فائل اپلوڈر (سائز کی لمٹ میسج کے ساتھ)
uploaded_file = st.file_uploader("اپنی ویڈیو فائل منتخب کریں", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    # ویڈیو کا پری ویو دکھانا
    st.video(uploaded_file)
    st.info(f"فائل کا نام: {uploaded_file.name}")
    
    # اپلوڈ بٹن
    if st.button("🚀 پاور ورڈز کے ساتھ یوٹیوب پر بھیجیں"):
        with st.spinner('براہ کرم انتظار کریں، آپ کی ویڈیو پروسیس ہو رہی ہے...'):
            # آپ کا Make.com ویب ہک لنک
            webhook_url = "https://hook.us2.make.com/zxh2tmrxbw43d0m7r0noijxu6213mvqo"
            
            # رینڈم پاور ورڈ منتخب کرنا اور نیا نام بنانا
            selected_word = random.choice(power_words)
            new_filename = f"{selected_word} - {uploaded_file.name}"
            
            # ڈیٹا کو تیار کرنا
            files = {
                "file": (new_filename, uploaded_file.getvalue(), uploaded_file.type)
            }
            payload = {"filename": new_filename}
            
            try:
                # ٹائم آؤٹ (Timeout) کے ساتھ ڈیٹا بھیجنا تاکہ 410 ایرر نہ آئے
                response = requests.post(webhook_url, files=files, data=payload, timeout=60)
                
                if response.status_code == 200:
                    st.success(f"✅ مبارک ہو! ویڈیو '{selected_word}' ٹیگ کے ساتھ کامیابی سے بھیج دی گئی۔")
                    st.balloons() # کامیابی پر اینیمیشن
                elif response.status_code == 413:
                    st.error("❌ فائل کا سائز بہت بڑا ہے۔ براہ کرم چھوٹی ویڈیو آزمائیں۔")
                else:
                    st.error(f"❌ سرور کا مسئلہ (Error {response.status_code})۔ دوبارہ کوشش کریں۔")
            
            except requests.exceptions.Timeout:
                st.error("⚠️ کنکشن کا وقت ختم ہو گیا۔ انٹرنیٹ چیک کریں یا دوبارہ کوشش کریں۔")
            except Exception as e:
                st.error(f"⚠️ ایک غیر متوقع غلطی ہوئی: {e}")

else:
    st.write("💡 ابھی تک کوئی فائل منتخب نہیں کی گئی۔")

st.markdown("---")
st.caption("Developed for Automating YouTube Uploads")
