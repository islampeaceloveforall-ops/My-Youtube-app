import streamlit as st
import requests

st.set_page_config(page_title="One-Click YouTube", page_icon="🚀")
st.title("🎬 یوٹیوب ون کلک اپلوڈر")

uploaded_file = st.file_uploader("ویڈیو منتخب کریں", type=["mp4", "mov", "avi"])

if st.button("پاور ورڈز کے ساتھ اپلوڈ کریں"):
    if uploaded_file is not None:
        with st.spinner('پروسیس ہو رہا ہے...'):
            # یہاں اپنا Make.com والا لنک ڈالیں
            webhook_url = "https://hook.us1.make.com/آپ_کا_اپنا_لنک"
            
            files = {"file": uploaded_file.getvalue()}
            data = {"filename": uploaded_file.name}
            
            response = requests.post(webhook_url, files=files, data=data)
            if response.status_code == 200:
                st.success("✅ ویڈیو کامیابی سے بھیج دی گئی ہے!")
            else:
                st.error("❌ مسئلہ آگیا، دوبارہ چیک کریں۔")
    else:
        st.warning("⚠️ پہلے ویڈیو فائل منتخب کریں۔")
