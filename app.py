import streamlit as st
import requests
import random

st.set_page_config(page_title="YouTube Uploader", page_icon="🚀")
st.title("🎬 یوٹیوب ون کلک اپلوڈر")

power_words = ["AMAZING", "SHOCKING", "MUST WATCH", "UNBELIEVABLE", "SECRET"]

uploaded_file = st.file_uploader("ویڈیو منتخب کریں", type=["mp4", "mov", "avi"])

if st.button("پاور ورڈز کے ساتھ اپلوڈ کریں"):
    if uploaded_file is not None:
        with st.spinner('ویڈیو پروسیس ہو رہی ہے...'):
            # آپ کا صحیح لنک یہاں ہے
            webhook_url = "https://hook.us2.make.com/zxh2tmrxbw43d0m7r0noijxu6213mvqo"
            
            word = random.choice(power_words)
            new_name = f"{word} - {uploaded_file.name}"
            
            files = {"file": uploaded_file.getvalue()}
            data = {"filename": new_name}
            
            try:
                r = requests.post(webhook_url, files=files, data=data)
                st.success(f"✅ کامیابی! فائل '{word}' کے ساتھ بھیج دی گئی!")
            except:
                st.error("❌ کنکشن کا مسئلہ ہے۔")
    else:
        st.warning("⚠️ پہلے ویڈیو فائل منتخب کریں۔")
