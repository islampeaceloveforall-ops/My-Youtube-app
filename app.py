import streamlit as st
import requests

st.title("YouTube Uploader")

webhook_url = "https://hook.us2.make.com/zxh2tmrxbw43d0m7r0noijxu6213mvqo"

file = st.file_uploader("Select Video")

if st.button("Upload"):
    if file:
        res = requests.post(webhook_url, files={"file": file.getvalue()}, data={"name": file.name})
        if res.status_code == 200:
            st.success("Sent to Make.com!")
        else:
            st.error(f"Error: {res.status_code}")
