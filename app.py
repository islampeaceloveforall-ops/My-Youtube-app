import streamlit as st
import requests
import random

st.set_page_config(page_title="YouTube Uploader", page_icon="🚀")
st.title("🎬 یوٹیوب ون کلک اپلوڈر")

# پاور ورڈز
power_words = ["AMAZING", "SHOCKING", "MUST WATCH", "UNBELIEVABLE", "SECRET"]

# فائل اپلوڈر کو ایک متغیر (Variable) میں رکھیں
uploaded_file = st.file_uploader("ویڈیو منتخب کریں", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    st.video(uploaded_file) # یہ لائن ویڈیو دکھائے گی تاکہ کنفرم ہو سکے کہ فائل لوڈ ہو گئی ہے
    
    if st.button("پاور ورڈز کے ساتھ اپلوڈ کریں"):
        with st.spinner('ویڈیو پروسیس ہو رہی ہے...'):
            webhook_url = "https://hook.us2.make.com/zxh2tmrxbw43d0m7r0noijxu6213mvqo"
            
            word = random.choice(power_words)
            new_name = f"{word} - {uploaded_file.name}"
            
            files = {"file": (new_name, uploaded_file.getvalue(), uploaded_file.type)}
            data = {"filename": new_name}
            
            try:
                r = requests.post(webhook_url, files=files, data=data)
                if r.status_code == 200:
                    st.success(f"✅ کامیابی! فائل '{word}' کے ساتھ بھیج دی گئی!")
                else:
                    st.error(f"❌ سرور ایرر: {r.status_code}")
            except Exception as e:
                st.error(f"❌ نیٹ ورک ایرر: {e}")
else:
    st.info("💡 اوپر 'Browse files' پر کلک کر کے ویڈیو سلیکٹ کریں۔")
