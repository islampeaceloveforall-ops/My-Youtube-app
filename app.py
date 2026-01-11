import streamlit as st
import requests
import os
from typing import Optional

# =================== تنظیمات (Configurations) ===================
# یہاں آپ اپنا نیا Make.com ویب ہک URL ڈالیں
WEBHOOK_URL = "https://hook.us2.make.com/آپکا_نیا_ویب_ہک_یہاں_ڈالیں"
MAX_FILE_SIZE_MB = 500  # زیادہ سے زیادہ فائل سائز (MB میں)
ALLOWED_EXTENSIONS = ['.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv']

# =================== ہیلپر فنکشنز ===================
def validate_file(file) -> Optional[str]:
    """
    فائل کی جانچ پڑتال کرتا ہے
    واپسی: غلطی کا پیغام یا None اگر سب ٹھیک ہے
    """
    if file is None:
        return "براہ کرم پہلے ایک فائل منتخب کریں"
    
    # فائل کا ایکسٹینشن چیک کریں
    file_extension = os.path.splitext(file.name)[1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        return f"غیر مجاز فائل کی قسم۔ صرف یہ ایکسٹینشنز قبول ہیں: {', '.join(ALLOWED_EXTENSIONS)}"
    
    # فائل کا سائز چیک کریں
    file_size_mb = file.size / (1024 * 1024)  # بائٹس سے MB میں
    if file_size_mb > MAX_FILE_SIZE_MB:
        return f"فائل کا سائز بہت بڑا ہے۔ زیادہ سے زیادہ اجازت: {MAX_FILE_SIZE_MB} MB"
    
    return None

def send_to_make(file) -> dict:
    """
    Make.com کو فائل بھیجتا ہے
    واپسی: نتیجہ کا ڈکشنری
    """
    try:
        # فائل کو مناسب طریقے سے بھیجیں
        files = {"file": (file.name, file.getvalue(), file.type)}
        data = {"filename": file.name, "size": file.size}
        
        response = requests.post(
            WEBHOOK_URL, 
            files=files, 
            data=data,
            timeout=30  # 30 سیکنڈ کا ٹائم آؤٹ
        )
        
        return {
            "success": response.status_code == 200,
            "status_code": response.status_code,
            "message": response.text,
            "error": None
        }
        
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "status_code": 408,
            "message": "Request timeout",
            "error": "Make.com نے جواب نہیں دیا۔ براہ کرم دوبارہ کوشش کریں۔"
        }
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "status_code": 0,
            "message": "Connection failed",
            "error": "نیٹ ورک کنکشن نہیں ہو سکا۔ براہ کرم اپنا انٹرنیٹ چیک کریں۔"
        }
    except Exception as e:
        return {
            "success": False,
            "status_code": 500,
            "message": "Internal error",
            "error": f"غیر متوقع غلطی: {str(e)}"
        }

# =================== Streamlit UI ===================
st.set_page_config(
    page_title="YouTube Uploader Pro",
    page_icon="📤",
    layout="wide"
)

# سائیڈ بار میں معلومات
with st.sidebar:
    st.header("📋 معلومات")
    st.markdown(f"""
    **قبول شدہ فائل اقسام:**
    {', '.join(ALLOWED_EXTENSIONS)}
    
    **زیادہ سے زیادہ سائز:** {MAX_FILE_SIZE_MB} MB
    
    **Make.com ویب ہک:** {'✅ فعال' if WEBHOOK_URL.startswith('https://') else '❌ ترتیب دیں'}
    """)
    
    if not WEBHOOK_URL.startswith('https://hook.us2.make.com/'):
        st.warning("""
        **ہدایت:** 
        1. Make.com پر جائیں
        2. نیا ویب ہک بنائیں
        3. اوپر والی لائن میں اس کا URL ڈالیں
        """)

# مین صفحہ
st.title("📤 YouTube Uploader Pro")
st.markdown("---")

# دو کالم بنائیں
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📁 ویڈیو فائل منتخب کریں")
    file = st.file_uploader(
        "فائل منتخب کرنے کے لیے یہاں کلک کریں",
        type=[ext.replace('.', '') for ext in ALLOWED_EXTENSIONS],
        help=f"صرف ویڈیو فائلز، زیادہ سے زیادہ {MAX_FILE_SIZE_MB}MB"
    )
    
    if file:
        # فائل کی معلومات دکھائیں
        file_size_mb = file.size / (1024 * 1024)
        file_extension = os.path.splitext(file.name)[1].lower()
        
        st.success(f"✅ فائل منتخب ہو گئی ہے")
        st.info(f"""
        **نام:** {file.name}
        **سائز:** {file_size_mb:.2f} MB
        **قسم:** {file_extension}
        """)
        
        # اپ لوڈ بٹن
        upload_button = st.button(
            "🚀 Make.com پر اپ لوڈ کریں",
            type="primary",
            use_container_width=True
        )
        
        if upload_button:
            # فائل کی جانچ
            validation_error = validate_file(file)
            
            if validation_error:
                st.error(f"❌ {validation_error}")
            else:
                # پیشرفت بار دکھائیں
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # مرحلہ 1: فائل کی جانچ
                status_text.text("فائل کی جانچ پڑتال ہو رہی ہے...")
                progress_bar.progress(25)
                
                # مرحلہ 2: Make.com کو بھیجنا
                status_text.text("Make.com کو بھیجا جا رہا ہے...")
                progress_bar.progress(50)
                
                # فائل بھیجیں
                result = send_to_make(file)
                progress_bar.progress(75)
                
                # نتیجہ دکھائیں
                status_text.text("نتیجہ پر کارروائی ہو رہی ہے...")
                progress_bar.progress(100)
                
                if result["success"]:
                    st.success("🎉 فائل کامیابی سے Make.com پر بھیج دی گئی ہے!")
                    
                    # اضافی معلومات
                    with st.expander("📊 تفصیلی معلومات"):
                        st.json(result, expanded=False)
                        
                    # دوبارہ بٹن
                    if st.button("🔄 نیویڈیو اپ لوڈ کریں"):
                        st.rerun()
                else:
                    st.error(f"❌ اپ لوڈ ناکام ہو گیا: {result.get('error', 'نامعلوم غلطی')}")
                    
                    with st.expander("🔍 مسلے کی تفصیل"):
                        st.write(f"**سٹیٹس کوڈ:** {result['status_code']}")
                        st.write(f"**مکمل جواب:** {result['message']}")
                        st.write(f"**غلطی:** {result['error']}")
                    
                    # ٹربل شوٹنگ ٹپس
                    st.warning("""
                    **ٹربل شوٹنگ:**
                    1. Make.com ویب ہک URL چیک کریں
                    2. انٹرنیٹ کنکشن چیک کریں
                    3. فائل کا سائز Limit سے چھوٹا ہونا چاہیے
                    4. Make.com سیناریو فعال ہونا چاہیے
                    """)

with col2:
    st.subheader("📋 ہدایات")
    st.markdown("""
    1. **فائل منتخب کریں** بائیں طرف
    2. **Make.com پر اپ لوڈ کریں** بٹن دبائیں
    3. **نتیجہ کا انتظار کریں**
    
    **خصوصیات:**
    - ✅ فائل کی قسم کی جانچ
    - ✅ سائز Limit
    - ✅ پیشرفت بار
    - ✅ غلطی کا انتظام
    - ✅ تفصیلی رپورٹس
    """)
    
    # Make.com کنفیگریشن سیکشن
    st.subheader("⚙️ Make.com ترتیب")
    
    if WEBHOOK_URL == "https://hook.us2.make.com/آپکا_نیا_ویب_ہک_یہاں_ڈالیں":
        st.error("⚠️ براہ کرم پہلے Make.com کا ویب ہک URL ڈالیں")
        new_webhook = st.text_input(
            "نیا ویب ہک URL:",
            placeholder="https://hook.us2.make.com/..."
        )
        
        if new_webhook:
            st.code(f"""
            # تبدیلی کریں لائن 8 پر:
            WEBHOOK_URL = "{new_webhook}"
            """, language="python")
            st.success("اب اوپر والا کوڈ اپ ڈیٹ کریں")

# فٹر
st.markdown("---")
st.caption("© YouTube Uploader Pro | Powered by Streamlit & Make.com")

# لاگنگ (ڈیبگ کے لیے)
if st.sidebar.checkbox("🔧 ڈیبگ معلومات دکھائیں"):
    st.sidebar.subheader("ڈیبگ معلومات")
    st.sidebar.write(f"**ویب ہک URL:** {WEBHOOK_URL[:50]}...")
    st.sidebar.write(f"**فائل سائز Limit:** {MAX_FILE_SIZE_MB} MB")
    st.sidebar.write(f**قبول شدہ ایکسٹینشنز:** {len(ALLOWED_EXTENSIONS)}")
