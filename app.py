"""
███████╗██╗  ██╗ █████╗ ██╗  ██╗██╗██████╗      ██████╗ ██████╗  ██████╗ 
██╔════╝██║  ██║██╔══██╗██║  ██║██║██╔══██╗    ██╔════╝██╔═══██╗██╔═══██╗
███████╗███████║███████║███████║██║██║  ██║    ██║     ██║   ██║██║   ██║
╚════██║██╔══██║██╔══██║██╔══██║██║██║  ██║    ██║     ██║   ██║██║   ██║
███████║██║  ██║██║  ██║██║  ██║██║██████╔╝    ╚██████╗╚██████╔╝╚██████╔╝
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═════╝      ╚═════╝ ╚═════╝  ╚═════╝ 

🎬 MAZARI YOUTUBE UPLOADER PRO - پیشہ ورانہ ویڈیو پروسیسنگ پلیٹ فارم
📧 ڈویلپر: شاہد احمد مزاری | 📱 وٹس ایپ: 03326179672 | ✉️ ای میل: shahidahmadmazari@gmail.com
"""

import streamlit as st
import requests
import random
import os
import json
import time
import hashlib
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from pathlib import Path
import mimetypes
from PIL import Image
import io
import base64
from streamlit_lottie import st_lottie
import logging

# ==================== تنظیمات آغاز ====================
# لاگنگ کا نظام
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mazari_uploader.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ڈویلپر کی معلومات - مرکزی تشہیر
class DeveloperInfo:
    NAME = "شاہد احمد مزاری"
    WHATSAPP = "03326179672"
    EMAIL = "shahidahmadmazari@gmail.com"
    COMPANY = "مزاری ڈیجیٹل سولوشنز"
    TAGLINE = "پیشہ ورانہ ویڈیو پروسیسنگ اور ڈیجیٹل مارکیٹنگ"
    WEBSITE = "mazaridigital.com (جلد آرہا ہے)"
    ADDRESS = "لاہور، پاکستان"
    
    @staticmethod
    def get_contact_cards():
        return {
            "whatsapp": f"https://wa.me/{DeveloperInfo.WHATSAPP}",
            "email": f"mailto:{DeveloperInfo.EMAIL}",
            "phone": f"tel:{DeveloperInfo.WHATSAPP}",
            "portfolio": "#"
        }

# ایپ کی جامع ترتیبات
class AppConfig:
    # ویب ہک یوآرایل (آپ اپنی ضرورت کے مطابق تبدیل کریں)
    WEBHOOK_URL = "https://hook.us2.make.com/zxh2tmrxbw43d0m7r0noijxu6213mvqo"
    
    # فائل کی حد بندی
    MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024  # 2GB
    ALLOWED_EXTENSIONS = ["mp4", "mov", "avi", "mkv", "wmv", "flv", "webm", "mpeg", "mpg", "m4v"]
    
    # پاور ورڈز کی جامع فہرست
    POWER_WORDS = [
        "🔥 وائرل ویڈیو", "⚡ فوری دیکھیں", "🎬 سنیماٹک", "💎 پریمیم", 
        "🚀 ایپک کانٹینٹ", "🌟 حیرت انگیز", "🤯 دماغ ہلا دینے والا", 
        "💯 اعلیٰ معیار", "👑 بادشاہ", "📈 تیزی سے بڑھ رہا", 
        "🎯 ہدف حاصل", "💥 دھماکہ خیز", "✨ خصوصی", "🏆 فاتح", 
        "💼 پیشہ ورانہ", "🌐 عالمی پہنچ", "📊 ڈیٹا سے چلنے والا",
        "🤝 تعاون", "🎨 تخلیقی", "🚀 نئی ٹیکنالوجی", "💡 انقلابی",
        "🏅 بیسٹ سیلر", "⭐ 5 سٹار ریٹڈ", "🔝 ٹاپ رینکنگ",
        "🎪 شو اسٹاپر", "🌪️ طوفان", "💰 قیمتی", "🔮 مستقبل بین",
        "🏰 شاہکار", "🎭 ڈرامائی", "🌅 یادگار", "⚓ قابل اعتماد"
    ]
    
    # رنگوں کا اسکیم
    COLOR_SCHEME = {
        "primary": "#1E3A8A",      # نیلا
        "secondary": "#059669",    # سبز
        "accent": "#7C3AED",       # جامنی
        "warning": "#F59E0B",      # سنہری
        "danger": "#DC2626",       # سرخ
        "dark": "#1F2937",         # گہرا
        "light": "#F9FAFB"         # ہلکا
    }
    
    # اپ لوڈ کی ترتیبات
    UPLOAD_SETTINGS = {
        "auto_watermark": True,
        "watermark_text": "Mazari Digital Solutions",
        "auto_compress": False,
        "add_timestamp": True,
        "generate_thumbnail": False
    }

# ==================== اعانت کنندہ افعال ====================
class HelperFunctions:
    @staticmethod
    def load_lottie_url(url: str):
        """Lottie animations لوڈ کرنے کا فنکشن"""
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return r.json()
        except:
            return None
    
    @staticmethod
    def get_file_icon(file_type: str):
        """فائل کی قسم کے مطابق آئیکن واپس کرتا ہے"""
        icons = {
            "video": "🎬",
            "image": "🖼️",
            "document": "📄",
            "audio": "🎵",
            "archive": "📦"
        }
        return icons.get(file_type, "📁")
    
    @staticmethod
    def format_file_size(size_bytes):
        """فائل سائز کو پڑھنے کے قابل شکل میں تبدیل کرتا ہے"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
    
    @staticmethod
    def generate_file_id(file_content):
        """فائل کے لیے منفرد ID بناتا ہے"""
        return hashlib.sha256(file_content).hexdigest()[:16]
    
    @staticmethod
    def validate_file(file, max_size):
        """فائل کی مکمل تصدیق کرتا ہے"""
        errors = []
        
        # سائز کی تصدیق
        if file.size > max_size:
            errors.append(f"❌ فائل سائز {HelperFunctions.format_file_size(file.size)} ہے، جبکہ حد {HelperFunctions.format_file_size(max_size)} ہے۔")
        
        # ایکسٹینشن کی تصدیق
        extension = Path(file.name).suffix.lower()[1:] if '.' in file.name else ''
        if extension not in AppConfig.ALLOWED_EXTENSIONS:
            errors.append(f"❌ غیر معاون فائل فارمیٹ: .{extension}")
        
        return errors
    
    @staticmethod
    def create_progress_widget():
        """پروگرس بار ویجٹ بناتا ہے"""
        progress_bar = st.progress(0)
        status_text = st.empty()
        return progress_bar, status_text
    
    @staticmethod
    def update_progress(progress_bar, status_text, value, message):
        """پروگرس بار اپ ڈیٹ کرتا ہے"""
        progress_bar.progress(value)
        status_text.info(f"🔄 {message}... {value}%")

# ==================== سیشن مینجمنٹ ====================
class SessionManager:
    @staticmethod
    def initialize():
        """سیشن اسٹیٹ شروع کرتا ہے"""
        if 'uploads' not in st.session_state:
            st.session_state.uploads = []
        
        if 'stats' not in st.session_state:
            st.session_state.stats = {
                'total_uploads': 0,
                'total_size': 0,
                'successful': 0,
                'failed': 0,
                'daily_uploads': {}
            }
        
        if 'settings' not in st.session_state:
            st.session_state.settings = AppConfig.UPLOAD_SETTINGS.copy()
        
        if 'user_quota' not in st.session_state:
            st.session_state.user_quota = {
                'daily_limit': 20,
                'uploads_today': 0,
                'reset_time': datetime.now() + timedelta(days=1)
            }
    
    @staticmethod
    def add_upload_record(file_info):
        """اپ لوڈ ریکارڈ شامل کرتا ہے"""
        st.session_state.uploads.append(file_info)
        
        # اعداد و شمار اپ ڈیٹ کریں
        st.session_state.stats['total_uploads'] += 1
        st.session_state.stats['total_size'] += file_info.get('size', 0)
        
        if file_info.get('status') == 'success':
            st.session_state.stats['successful'] += 1
        else:
            st.session_state.stats['failed'] += 1
        
        # روزانہ اپ لوڈ کاؤنٹ
        today = datetime.now().date()
        if today not in st.session_state.stats['daily_uploads']:
            st.session_state.stats['daily_uploads'][today] = 0
        st.session_state.stats['daily_uploads'][today] += 1
        
        # کوٹا اپ ڈیٹ کریں
        st.session_state.user_quota['uploads_today'] += 1
    
    @staticmethod
    def check_quota():
        """موجودہ کوٹا چیک کرتا ہے"""
        # اگر ری سیٹ کا وقت گزر گیا ہو
        if datetime.now() > st.session_state.user_quota['reset_time']:
            st.session_state.user_quota['uploads_today'] = 0
            st.session_state.user_quota['reset_time'] = datetime.now() + timedelta(days=1)
        
        remaining = st.session_state.user_quota['daily_limit'] - st.session_state.user_quota['uploads_today']
        return max(0, remaining)

# ==================== ویڈیو پروسیسر ====================
class VideoProcessor:
    def __init__(self):
        self.config = AppConfig()
    
    def process_video(self, file, power_word, custom_name=None):
        """ویڈیو فائل کو پروسیس کرتا ہے"""
        try:
            # فائل کا مواد پڑھیں
            file_content = file.getvalue()
            
            # فائنل فائل نام بنائیں
            if custom_name:
                final_name = custom_name
            else:
                original_name = Path(file.name).stem
                extension = Path(file.name).suffix
                final_name = f"{power_word} - {original_name}{extension}"
            
            # میٹا ڈیٹا تیار کریں
            metadata = {
                "filename": final_name,
                "original_name": file.name,
                "size": file.size,
                "file_id": HelperFunctions.generate_file_id(file_content),
                "upload_time": datetime.now().isoformat(),
                "developer": DeveloperInfo.NAME,
                "contact_whatsapp": DeveloperInfo.WHATSAPP,
                "contact_email": DeveloperInfo.EMAIL,
                "power_word": power_word,
                "watermark": st.session_state.settings.get('watermark_text', ''),
                "app_version": "3.0.0",
                "upload_source": "Mazari YouTube Uploader Pro"
            }
            
            return final_name, file_content, metadata
            
        except Exception as e:
            logger.error(f"Video processing error: {e}")
            raise

# ==================== ویب ہک مینیجر ====================
class WebhookManager:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url
        self.timeout = 300  # 5 منٹ
    
    def send_file(self, filename, file_content, metadata):
        """فائل کو ویب ہک پر بھیجتا ہے"""
        try:
            # فائل تیار کریں
            files = {
                'file': (filename, file_content, 'video/mp4')
            }
            
            # ڈیٹا تیار کریں
            data = {
                'metadata': json.dumps(metadata, ensure_ascii=False)
            }
            
            # POST request بھیجیں
            response = requests.post(
                self.webhook_url,
                files=files,
                data=data,
                timeout=self.timeout
            )
            
            # رسپانس لوگ کریں
            logger.info(f"Webhook response: {response.status_code}")
            
            return {
                'success': response.status_code == 200,
                'status_code': response.status_code,
                'message': response.text,
                'metadata': metadata
            }
            
        except requests.exceptions.Timeout:
            logger.error("Webhook request timeout")
            return {
                'success': False,
                'error': 'timeout',
                'message': 'سرور کا جواب موصول نہیں ہوا۔'
            }
        except Exception as e:
            logger.error(f"Webhook error: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'نا معلوم خرابی'
            }

# ==================== ڈیش بورڈ کمپوننٹس ====================
class DashboardComponents:
    @staticmethod
    def create_header():
        """مرکزی ہیڈر بناتا ہے"""
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown(f"""
            <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, {AppConfig.COLOR_SCHEME['primary']}, {AppConfig.COLOR_SCHEME['accent']}); 
                     border-radius: 20px; color: white; margin-bottom: 2rem;">
                <h1 style="font-size: 3rem; margin-bottom: 0.5rem;">🎬 مزاری YouTube اپ لوڈر</h1>
                <h3 style="font-weight: 300; margin-bottom: 1rem;">پیشہ ورانہ ویڈیو پروسیسنگ پلیٹ فارم</h3>
                <div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 10px; display: inline-block;">
                    <p style="margin: 0; font-size: 1.1rem;">
                        <strong>👨‍💼 ڈویلپر:</strong> {DeveloperInfo.NAME}<br>
                        <strong>📱 رابطہ:</strong> {DeveloperInfo.WHATSAPP}<br>
                        <strong>✉️ ای میل:</strong> {DeveloperInfo.EMAIL}
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def create_stats_cards():
        """اعداد و شمار کے کارڈز بناتا ہے"""
        cols = st.columns(4)
        
        with cols[0]:
            st.metric(
                "📊 کل اپ لوڈز",
                st.session_state.stats['total_uploads'],
                help="اب تک کی کل اپ لوڈ شدہ فائلز"
            )
        
        with cols[1]:
            st.metric(
                "💾 کل ڈیٹا",
                HelperFunctions.format_file_size(st.session_state.stats['total_size']),
                help="کل اپ لوڈ شدہ ڈیٹا کا سائز"
            )
        
        with cols[2]:
            success_rate = 0
            if st.session_state.stats['total_uploads'] > 0:
                success_rate = (st.session_state.stats['successful'] / st.session_state.stats['total_uploads']) * 100
            st.metric(
                "✅ کامیابی کی شرح",
                f"{success_rate:.1f}%",
                help="کامیاب اپ لوڈز کا فیصد"
            )
        
        with cols[3]:
            remaining = SessionManager.check_quota()
            st.metric(
                "🎯 باقی کوٹا",
                f"{remaining}/{st.session_state.user_quota['daily_limit']}",
                help="آج کے لیے باقی اپ لوڈز"
            )
    
    @staticmethod
    def create_contact_section():
        """رابطے کا سیکشن بناتا ہے"""
        st.markdown("---")
        st.markdown("### 📞 فوری رابطہ")
        
        contacts = DeveloperInfo.get_contact_cards()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <a href="{contacts['whatsapp']}" target="_blank" style="text-decoration: none;">
                <div style="background: #25D366; color: white; padding: 1rem; border-radius: 10px; text-align: center; cursor: pointer; transition: transform 0.3s;">
                    <div style="font-size: 2rem;">📱</div>
                    <strong>وٹس ایپ</strong>
                    <p style="font-size: 0.8rem; margin: 0;">{DeveloperInfo.WHATSAPP}</p>
                </div>
            </a>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <a href="{contacts['email']}" style="text-decoration: none;">
                <div style="background: #EA4335; color: white; padding: 1rem; border-radius: 10px; text-align: center; cursor: pointer; transition: transform 0.3s;">
                    <div style="font-size: 2rem;">✉️</div>
                    <strong>ای میل</strong>
                    <p style="font-size: 0.8rem; margin: 0;">{DeveloperInfo.EMAIL}</p>
                </div>
            </a>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <a href="{contacts['phone']}" style="text-decoration: none;">
                <div style="background: #4285F4; color: white; padding: 1rem; border-radius: 10px; text-align: center; cursor: pointer; transition: transform 0.3s;">
                    <div style="font-size: 2rem;">📞</div>
                    <strong>فون کال</strong>
                    <p style="font-size: 0.8rem; margin: 0;">{DeveloperInfo.WHATSAPP}</p>
                </div>
            </a>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <a href="#portfolio" style="text-decoration: none;">
                <div style="background: {AppConfig.COLOR_SCHEME['accent']}; color: white; padding: 1rem; border-radius: 10px; text-align: center; cursor: pointer; transition: transform 0.3s;">
                    <div style="font-size: 2rem;">📁</div>
                    <strong>پورٹ فولیو</strong>
                    <p style="font-size: 0.8rem; margin: 0;">{DeveloperInfo.COMPANY}</p>
                </div>
            </a>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def create_analytics_charts():
        """تجزیاتی چارٹس بناتا ہے"""
        if st.session_state.stats['total_uploads'] == 0:
            st.info("📈 ابھی تک کافی ڈیٹا موجود نہیں ہے۔ پہلی ویڈیو اپ لوڈ کریں!")
            return
        
        # روزانہ اپ لوڈز کا چارٹ
        daily_data = st.session_state.stats['daily_uploads']
        if daily_data:
            df_daily = pd.DataFrame(list(daily_data.items()), columns=['تاریخ', 'تعداد'])
            fig = px.line(df_daily, x='تاریخ', y='تعداد', 
                         title='📅 روزانہ اپ لوڈز کا گراف',
                         line_shape='spline')
            st.plotly_chart(fig, use_container_width=True)
        
        # پاور ورڈز کا تجزیہ
        if st.session_state.uploads:
            power_words_used = [upload.get('power_word', 'نامعلوم') 
                              for upload in st.session_state.uploads 
                              if upload.get('power_word')]
            
            if power_words_used:
                from collections import Counter
                word_counts = Counter(power_words_used)
                top_words = dict(word_counts.most_common(10))
                
                fig2 = px.bar(x=list(top_words.keys()), y=list(top_words.values()),
                             title='🎯 سب سے زیادہ استعمال ہونے والے پاور ورڈز',
                             labels={'x': 'پاور ورڈ', 'y': 'تعداد'})
                st.plotly_chart(fig2, use_container_width=True)

# ==================== مرکزی ایپلیکیشن ====================
class MazariYouTubeUploader:
    def __init__(self):
        self.setup_page_config()
        SessionManager.initialize()
        self.processor = VideoProcessor()
        self.webhook_manager = WebhookManager(AppConfig.WEBHOOK_URL)
        
    def setup_page_config(self):
        """صفحہ کی ترتیبات طے کرتا ہے"""
        st.set_page_config(
            page_title=f"{DeveloperInfo.COMPANY} | {DeveloperInfo.NAME}",
            page_icon="🚀",
            layout="wide",
            initial_sidebar_state="expanded",
            menu_items={
                'Get Help': f'https://wa.me/{DeveloperInfo.WHATSAPP}',
                'Report a bug': f'mailto:{DeveloperInfo.EMAIL}',
                'About': f'''
                ## {DeveloperInfo.COMPANY}
                
                **ڈویلپر:** {DeveloperInfo.NAME}
                **رابطہ:** {DeveloperInfo.WHATSAPP}
                **ای میل:** {DeveloperInfo.EMAIL}
                **کمپنی:** {DeveloperInfo.COMPANY}
                **ورژن:** 3.0.0
                
                یہ ایپ پیشہ ورانہ ویڈیو اپ لوڈنگ اور 
                پروسیسنگ کے لیے بنائی گئی ہے۔
                '''
            }
        )
        
        # کسٹم CSS شامل کریں
        self.inject_custom_css()
    
    def inject_custom_css(self):
        """اپنی مرضی کا CSS شامل کرتا ہے"""
        st.markdown(f"""
        <style>
            /* بنیادی ترتیبات */
            .stApp {{
                background: linear-gradient(135deg, {AppConfig.COLOR_SCHEME['light']} 0%, #ffffff 100%);
            }}
            
            /* ہیڈنگز */
            h1, h2, h3, h4, h5, h6 {{
                font-family: 'Noto Sans Arabic', 'Segoe UI', sans-serif;
                color: {AppConfig.COLOR_SCHEME['primary']};
            }}
            
            /* کارڈز */
            .custom-card {{
                background: white;
                padding: 1.5rem;
                border-radius: 15px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.08);
                border-left: 5px solid {AppConfig.COLOR_SCHEME['secondary']};
                margin-bottom: 1rem;
                transition: transform 0.3s, box-shadow 0.3s;
            }}
            
            .custom-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 8px 30px rgba(0,0,0,0.12);
            }}
            
            /* بٹنز */
            .stButton > button {{
                background: linear-gradient(135deg, {AppConfig.COLOR_SCHEME['primary']} 0%, {AppConfig.COLOR_SCHEME['accent']} 100%);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 24px;
                font-weight: bold;
                transition: all 0.3s;
            }}
            
            .stButton > button:hover {{
                transform: scale(1.02);
                box-shadow: 0 5px 15px rgba({int(AppConfig.COLOR_SCHEME['primary'][1:3], 16)}, 
                                           {int(AppConfig.COLOR_SCHEME['primary'][3:5], 16)}, 
                                           {int(AppConfig.COLOR_SCHEME['primary'][5:7], 16)}, 0.3);
            }}
            
            /* پروگرس بار */
            .stProgress > div > div > div {{
                background: linear-gradient(90deg, {AppConfig.COLOR_SCHEME['secondary']}, {AppConfig.COLOR_SCHEME['accent']});
            }}
            
            /* ٹیبز */
            .stTabs [data-baseweb="tab-list"] {{
                gap: 2px;
            }}
            
            .stTabs [data-baseweb="tab"] {{
                border-radius: 10px 10px 0 0;
                padding: 10px 20px;
            }}
            
            /* فٹر */
            .footer {{
                background: {AppConfig.COLOR_SCHEME['dark']};
                color: white;
                padding: 2rem;
                border-radius: 15px;
                margin-top: 3rem;
                text-align: center;
            }}
        </style>
        """, unsafe_allow_html=True)
    
    def create_sidebar(self):
        """سائیڈبار بناتا ہے"""
        with st.sidebar:
            # ڈویلپر پروفائل
            st.markdown(f"""
            <div class="custom-card">
                <div style="text-align: center;">
                    <div style="font-size: 3rem; color: {AppConfig.COLOR_SCHEME['primary']};">👨‍💼</div>
                    <h3 style="margin: 0.5rem 0;">{DeveloperInfo.NAME}</h3>
                    <p style="color: {AppConfig.COLOR_SCHEME['secondary']}; font-weight: bold;">{DeveloperInfo.COMPANY}</p>
                    <p style="font-size: 0.9rem;">{DeveloperInfo.TAGLINE}</p>
                </div>
                <hr>
                <div>
                    <p><strong>📱:</strong> {DeveloperInfo.WHATSAPP}</p>
                    <p><strong>✉️:</strong> {DeveloperInfo.EMAIL}</p>
                    <p><strong>🏢:</strong> {DeveloperInfo.ADDRESS}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # کوٹا انفورمیشن
            remaining = SessionManager.check_quota()
            st.markdown(f"""
            <div class="custom-card">
                <h4>🎯 روزانہ کوٹا</h4>
                <div style="background: {AppConfig.COLOR_SCHEME['light']}; padding: 1rem; border-radius: 10px; text-align: center;">
                    <h1 style="margin: 0; color: {AppConfig.COLOR_SCHEME['primary']};">{remaining}</h1>
                    <p style="margin: 0;">/ {st.session_state.user_quota['daily_limit']} اپ لوڈز باقی</p>
                </div>
                <div style="margin-top: 1rem; height: 10px; background: #e5e7eb; border-radius: 5px;">
                    <div style="height: 100%; width: {min(100, (st.session_state.user_quota['uploads_today']/st.session_state.user_quota['daily_limit'])*100)}%; 
                         background: {AppConfig.COLOR_SCHEME['secondary']}; border-radius: 5px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # ترتیبات
            st.markdown("### ⚙️ ترتیبات")
            
            with st.expander("🎯 پاور ورڈز", expanded=True):
                custom_words = st.text_area(
                    "اپنے پاور ورڈز (ہر لائن پر ایک)",
                    value="\n".join(AppConfig.POWER_WORDS),
                    height=150
                )
                if st.button("💾 محفوظ کریں", use_container_width=True):
                    AppConfig.POWER_WORDS = [w.strip() for w in custom_words.split('\n') if w.strip()]
                    st.success("✅ پاور ورڈز محفوظ ہو گئے!")
            
            with st.expander("🔧 اپ لوڈ ترتیبات"):
                st.session_state.settings['auto_watermark'] = st.checkbox(
                    "خودکار واٹر مارک",
                    value=st.session_state.settings['auto_watermark']
                )
                
                if st.session_state.settings['auto_watermark']:
                    st.session_state.settings['watermark_text'] = st.text_input(
                        "واٹر مارک ٹیکسٹ",
                        value=st.session_state.settings.get('watermark_text', '')
                    )
                
                st.session_state.settings['add_timestamp'] = st.checkbox(
                    "ٹائم اسٹیمپ شامل کریں",
                    value=st.session_state.settings['add_timestamp']
                )
            
            # فائل سائز کی حد
            max_size_mb = st.slider(
                "📏 زیادہ سے زیادہ فائل سائز (MB)",
                min_value=50,
                max_value=4096,
                value=2048,
                step=50
            )
            AppConfig.MAX_FILE_SIZE = max_size_mb * 1024 * 1024
            
            # تاریخ صاف کریں
            st.markdown("---")
            if st.button("🗑️ تاریخ صاف کریں", use_container_width=True):
                st.session_state.uploads = []
                st.session_state.stats = {
                    'total_uploads': 0,
                    'total_size': 0,
                    'successful': 0,
                    'failed': 0,
                    'daily_uploads': {}
                }
                st.success("✅ تاریخ صاف ہو گئی!")
                st.rerun()
    
    def upload_tab(self):
        """اپ لوڈ ٹیب بناتا ہے"""
        st.markdown("### 📤 ویڈیو اپ لوڈ کریں")
        
        # فائل اپ لوڈر
        uploaded_file = st.file_uploader(
            "ویڈیو فائل منتخب کریں",
            type=AppConfig.ALLOWED_EXTENSIONS,
            help=f"حداکثر سائز: {HelperFunctions.format_file_size(AppConfig.MAX_FILE_SIZE)}"
        )
        
        if uploaded_file:
            # فائل کی تصدیق
            errors = HelperFunctions.validate_file(uploaded_file, AppConfig.MAX_FILE_SIZE)
            
            if errors:
                for error in errors:
                    st.error(error)
                return
            
            # فائل کی معلومات دکھائیں
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("#### 🎬 ویڈیو پریویو")
                st.video(uploaded_file)
                
                # تفصیلی معلومات
                with st.expander("📋 فائل کی تفصیلات", expanded=True):
                    info_col1, info_col2 = st.columns(2)
                    
                    with info_col1:
                        st.info(f"**نام:** {uploaded_file.name}")
                        st.info(f"**سائز:** {HelperFunctions.format_file_size(uploaded_file.size)}")
                        st.info(f"**قسم:** {uploaded_file.type if hasattr(uploaded_file, 'type') else 'نامعلوم'}")
                    
                    with info_col2:
                        file_id = HelperFunctions.generate_file_id(uploaded_file.getvalue())
                        st.info(f"**فائل ID:** `{file_id}`")
                        st.success("✅ فائل تصدیق شدہ")
                        
                        # کوٹا چیک
                        remaining = SessionManager.check_quota()
                        if remaining == 0:
                            st.error("❌ آج کا کوٹا ختم ہو گیا ہے!")
                        else:
                            st.success(f"✅ {remaining} اپ لوڈز باقی ہیں")
            
            with col2:
                # اپ لوڈ آپشنز
                st.markdown("#### ⚡ اپ لوڈ آپشنز")
                
                # پاور ورڈ منتخب کریں
                power_word_option = st.radio(
                    "پاور ورڈ کا انتخاب",
                    ["🎲 رینڈم منتخب کریں", "📝 فہرست سے منتخب کریں"],
                    horizontal=True
                )
                
                if power_word_option == "🎲 رینڈم منتخب کریں":
                    selected_word = random.choice(AppConfig.POWER_WORDS)
                    st.info(f"**منتخب شدہ:**\n\n### {selected_word}")
                else:
                    selected_word = st.selectbox(
                        "پاور ورڈ منتخب کریں",
                        AppConfig.POWER_WORDS
                    )
                
                # فائل نام کسٹمائزیشن
                st.markdown("---")
                st.markdown("#### 📝 فائل نام")
                
                default_name = f"{selected_word} - {uploaded_file.name}"
                custom_name = st.text_input(
                    "نیا فائل نام",
                    value=default_name
                )
                
                # اپ لوڈ بٹن
                remaining = SessionManager.check_quota()
                upload_disabled = remaining == 0
                
                upload_button = st.button(
                    f"🚀 اپ لوڈ کریں ({HelperFunctions.format_file_size(uploaded_file.size)})",
                    type="primary",
                    disabled=upload_disabled,
                    use_container_width=True
                )
                
                if upload_disabled:
                    st.warning("⚠️ آج کا کوٹا ختم ہو گیا ہے! کل دوبارہ کوشش کریں۔")
            
            # اپ لوڈ پروسیس
            if upload_button:
                self.process_upload(uploaded_file, selected_word, custom_name)
    
    def process_upload(self, file, power_word, custom_name):
        """اپ لوڈ پروسیس ہینڈل کرتا ہے"""
        try:
            # پروگرس بار شروع کریں
            progress_bar, status_text = HelperFunctions.create_progress_widget()
            
            # مرحلہ 1: فائل پروسیسنگ
            HelperFunctions.update_progress(progress_bar, status_text, 20, "فائل پروسیسنگ")
            final_name, file_content, metadata = self.processor.process_video(
                file, power_word, custom_name
            )
            
            # مرحلہ 2: ویب ہک پر بھیجنا
            HelperFunctions.update_progress(progress_bar, status_text, 60, "سرور پر بھیج رہا ہوں")
            result = self.webhook_manager.send_file(final_name, file_content, metadata)
            
            # مرحلہ 3: نتیجہ پروسیس کریں
            HelperFunctions.update_progress(progress_bar, status_text, 90, "نتیجہ پروسیس کر رہا ہوں")
            
            # مرحلہ 4: تکمیل
            HelperFunctions.update_progress(progress_bar, status_text, 100, "تکمیل")
            time.sleep(0.5)
            
            # پروگرس بار ہٹائیں
            progress_bar.empty()
            status_text.empty()
            
            # نتیجہ دکھائیں
            if result.get('success'):
                self.show_success_result(file, final_name, metadata, result)
            else:
                self.show_error_result(result)
                
        except Exception as e:
            st.error(f"❌ اپ لوڈ ناکام: {str(e)}")
            logger.error(f"Upload failed: {e}")
    
    def show_success_result(self, file, final_name, metadata, result):
        """کامیاب اپ لوڈ کا نتیجہ دکھاتا ہے"""
        st.balloons()
        
        # کامیابی کا کارڈ
        st.markdown(f"""
        <div class="custom-card" style="border-left: 5px solid {AppConfig.COLOR_SCHEME['secondary']};">
            <div style="text-align: center;">
                <div style="font-size: 4rem; color: {AppConfig.COLOR_SCHEME['secondary']};">✅</div>
                <h2 style="color: {AppConfig.COLOR_SCHEME['secondary']};">کامیابی! ویڈیو اپ لوڈ ہو گئی</h2>
            </div>
            <hr>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <div><strong>فائل نام:</strong></div><div>{final_name}</div>
                <div><strong>سائز:</strong></div><div>{HelperFunctions.format_file_size(file.size)}</div>
                <div><strong>پاور ورڈ:</strong></div><div>{metadata.get('power_word')}</div>
                <div><strong>وقت:</strong></div><div>{datetime.now().strftime('%H:%M:%S')}</div>
                <div><strong>واٹر مارک:</strong></div><div>{metadata.get('watermark', 'نہیں')}</div>
                <div><strong>اپ لوڈ از:</strong></div><div>{DeveloperInfo.NAME}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # سیشن اسٹیٹ اپ ڈیٹ کریں
        upload_record = {
            'filename': final_name,
            'original_name': file.name,
            'size': file.size,
            'power_word': metadata.get('power_word'),
            'timestamp': datetime.now().isoformat(),
            'status': 'success',
            'watermark': metadata.get('watermark', ''),
            'developer': DeveloperInfo.NAME
        }
        SessionManager.add_upload_record(upload_record)
        
        # ڈاؤن لوڈ بٹن
        st.download_button(
            label="📥 فائل ڈاؤن لوڈ کریں",
            data=file.getvalue(),
            file_name=final_name,
            mime=file.type if hasattr(file, 'type') else 'video/mp4',
            use_container_width=True
        )
    
    def show_error_result(self, result):
        """ناکام اپ لوڈ کا نتیجہ دکھاتا ہے"""
        st.markdown(f"""
        <div class="custom-card" style="border-left: 5px solid {AppConfig.COLOR_SCHEME['danger']};">
            <div style="text-align: center;">
                <div style="font-size: 4rem; color: {AppConfig.COLOR_SCHEME['danger']};">❌</div>
                <h2 style="color: {AppConfig.COLOR_SCHEME['danger']};">اپ لوڈ ناکام</h2>
            </div>
            <hr>
            <div style="text-align: center;">
                <p><strong>خرابی کی قسم:</strong> {result.get('error', 'نامعلوم')}</p>
                <p><strong>پیغام:</strong> {result.get('message', 'نامعلوم')}</p>
                <p><strong>حل:</strong> براہ کرم دوبارہ کوشش کریں یا {DeveloperInfo.WHATSAPP} پر رابطہ کریں۔</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # ناکام ریکارڈ شامل کریں
        upload_record = {
            'filename': 'نامعلوم',
            'timestamp': datetime.now().isoformat(),
            'status': 'failed',
            'error': result.get('error', 'نامعلوم')
        }
        SessionManager.add_upload_record(upload_record)
    
    def history_tab(self):
        """تاریخ ٹیب بناتا ہے"""
        st.markdown("### 📜 اپ لوڈ تاریخ")
        
        if not st.session_state.uploads:
            st.info("📝 ابھی تک کوئی فائل اپ لوڈ نہیں کی گئی۔")
            return
        
        # فلٹرز
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_status = st.selectbox("سٹیٹس", ["سب", "کامیاب", "ناکام"])
        with col2:
            filter_date = st.date_input("تاریخ سے")
        with col3:
            filter_power_word = st.selectbox("پاور ورڈ", ["سب"] + list(set([u.get('power_word', '') for u in st.session_state.uploads if u.get('power_word')])))
        
        # فلٹرڈ ڈیٹا
        filtered_uploads = st.session_state.uploads.copy()
        
        if filter_status != "سب":
            filtered_uploads = [u for u in filtered_uploads if u.get('status') == ('success' if filter_status == 'کامیاب' else 'failed')]
        
        if filter_power_word != "سب":
            filtered_uploads = [u for u in filtered_uploads if u.get('power_word') == filter_power_word]
        
        # ڈیٹا ٹیبل
        if filtered_uploads:
            df_data = []
            for upload in reversed(filtered_uploads[-100:]):  # آخری 100 ریکارڈز
                df_data.append([
                    upload.get('filename', 'نامعلوم'),
                    HelperFunctions.format_file_size(upload.get('size', 0)),
                    upload.get('power_word', 'نامعلوم'),
                    upload.get('timestamp', 'نامعلوم'),
                    "✅" if upload.get('status') == 'success' else "❌",
                    upload.get('developer', DeveloperInfo.NAME)
                ])
            
            df = pd.DataFrame(
                df_data,
                columns=['فائل نام', 'سائز', 'پاور ورڈ', 'وقت', 'سٹیٹس', 'ڈویلپر']
            )
            
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "سٹیٹس": st.column_config.TextColumn(width="small")
                }
            )
            
            # CSV ایکسپورٹ
            csv = df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📊 CSV ایکسپورٹ کریں",
                data=csv,
                file_name=f"mazari_history_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    def analytics_tab(self):
        """تجزیہ ٹیب بناتا ہے"""
        st.markdown("### 📈 تجزیات اور رپورٹس")
        
        if st.session_state.stats['total_uploads'] == 0:
            st.info("📊 تجزیہ کے لیے ڈیٹا موجود نہیں ہے۔ پہلی ویڈیو اپ لوڈ کریں!")
            return
        
        DashboardComponents.create_stats_cards()
        DashboardComponents.create_analytics_charts()
        
        # تفصیلی تجزیہ
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 کارکردگی کے اعداد و شمار")
            perf_data = {
                'متریک': ['کل اپ لوڈز', 'کامیاب', 'ناکام', 'اوسط سائز'],
                'قدر': [
                    st.session_state.stats['total_uploads'],
                    st.session_state.stats['successful'],
                    st.session_state.stats['failed'],
                    HelperFunctions.format_file_size(st.session_state.stats['total_size'] / st.session_state.stats['total_uploads'] if st.session_state.stats['total_uploads'] > 0 else 0)
                ]
            }
            st.dataframe(pd.DataFrame(perf_data), use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("#### 🎯 پاور ورڈ تجزیہ")
            if st.session_state.uploads:
                power_words = [u.get('power_word') for u in st.session_state.uploads if u.get('power_word')]
                if power_words:
                    from collections import Counter
                    word_counts = Counter(power_words)
                    top_5 = dict(word_counts.most_common(5))
                    
                    fig = go.Figure(data=[go.Pie(
                        labels=list(top_5.keys()),
                        values=list(top_5.values()),
                        hole=.3
                    )])
                    fig.update_layout(title="سب سے مقبول پاور ورڈز")
                    st.plotly_chart(fig, use_container_width=True)
    
    def info_tab(self):
        """معلومات ٹیب بناتا ہے"""
        st.markdown("### ℹ️ معلومات اور سپورٹ")
        
        DashboardComponents.create_contact_section()
        
        # خدمات
        st.markdown("---")
        st.markdown("### 🛠️ پیش کی جانے والی خدمات")
        
        services = [
            {"icon": "🎬", "title": "پیشہ ورانہ ویڈیو پروسیسنگ", "desc": "اعلیٰ معیار کی ویڈیو ایڈیٹنگ اور پروسیسنگ"},
            {"icon": "📈", "title": "YouTube چینل مینجمنٹ", "desc": "مکمل YouTube چینل کی دیکھ بھال اور ترقی"},
            {"icon": "🎯", "title": "ڈیجیٹل مارکیٹنگ", "desc": "موثر ڈیجیٹل مارکیٹنگ سٹریٹیجیز"},
            {"icon": "💻", "title": "کسٹم سافٹ ویئر ڈویلپمنٹ", "desc": "اپنی ضروریات کے مطابق سافٹ ویئر حل"},
            {"icon": "🤖", "title": "آٹومیشن سولوشنز", "desc": "کاروباری عمل کی خودکار کاری"},
            {"icon": "📊", "title": "ڈیٹا تجزیات", "desc": "ڈیٹا ڈرائیون ڈیسیژن بنانا"}
        ]
        
        cols = st.columns(3)
        for idx, service in enumerate(services):
            with cols[idx % 3]:
                st.markdown(f"""
                <div class="custom-card">
                    <div style="font-size: 2rem; text-align: center;">{service['icon']}</div>
                    <h4 style="text-align: center;">{service['title']}</h4>
                    <p style="text-align: center; font-size: 0.9rem;">{service['desc']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # رابطہ فارم
        st.markdown("---")
        st.markdown("### 📝 فوری رابطہ فارم")
        
        with st.form("contact_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("آپ کا نام")
                email = st.text_input("ای میل ایڈریس")
            with col2:
                phone = st.text_input("فون نمبر")
                service_type = st.selectbox("خدمت کی قسم", services, format_func=lambda x: x['title'])
            
            message = st.text_area("پیغام", height=150)
            
            submitted = st.form_submit_button("📤 پیغام بھیجیں")
            if submitted and name and message:
                st.success(f"✅ شکریہ {name}! جلد ہی آپ سے رابطہ کریں گے۔")
    
    def create_footer(self):
        """فٹر بناتا ہے"""
        st.markdown("---")
        st.markdown(f"""
        <div class="footer">
            <h3>{DeveloperInfo.COMPANY}</h3>
            <p>{DeveloperInfo.TAGLINE}</p>
            <div style="display: flex; justify-content: center; gap: 3rem; margin: 2rem 0; flex-wrap: wrap;">
                <div>
                    <strong>📞 رابطہ</strong><br>
                    {DeveloperInfo.WHATSAPP}<br>
                    {DeveloperInfo.EMAIL}
                </div>
                <div>
                    <strong>👨‍💼 ڈویلپر</strong><br>
                    {DeveloperInfo.NAME}<br>
                    {DeveloperInfo.ADDRESS}
                </div>
                <div>
                    <strong>📊 ایپ اسٹیٹس</strong><br>
                    {st.session_state.stats['total_uploads']} کل اپ لوڈز<br>
                    {HelperFunctions.format_file_size(st.session_state.stats['total_size'])} ڈیٹا
                </div>
            </div>
            <hr style="opacity: 0.3; width: 50%; margin: 1rem auto;">
            <p style="font-size: 0.9rem; opacity: 0.8;">
                © {datetime.now().year} {DeveloperInfo.COMPANY} - تمام حقوق محفوظ ہیں<br>
                یہ ایپ شاہد احمد مزاری نے ڈویلپ کی ہے | ورژن 3.0.0
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    def run(self):
        """ایپ چلاتا ہے"""
        # ہیڈر
        DashboardComponents.create_header()
        
        # سائیڈبار
        self.create_sidebar()
        
        # ٹیبز
        tab1, tab2, tab3, tab4 = st.tabs([
            "📤 اپ لوڈ ویڈیو", 
            "📜 تاریخ", 
            "📈 تجزیات", 
            "ℹ️ معلومات"
        ])
        
        with tab1:
            self.upload_tab()
        
        with tab2:
            self.history_tab()
        
        with tab3:
            self.analytics_tab()
        
        with tab4:
            self.info_tab()
        
        # فٹر
        self.create_footer()
        
        # لاگ پیغام
        logger.info(f"App accessed - Developer: {DeveloperInfo.NAME}")

# ==================== ایپ کا آغاز ====================
if __name__ == "__main__":
    try:
        app = MazariYouTubeUploader()
        app.run()
        
        # افتتاحی پیغام
        logger.info("=" * 50)
        logger.info(f"MAZARI YOUTUBE UPLOADER PRO STARTED")
        logger.info(f"Developer: {DeveloperInfo.NAME}")
        logger.info(f"Contact: {DeveloperInfo.WHATSAPP}")
        logger.info(f"Email: {DeveloperInfo.EMAIL}")
        logger.info("=" * 50)
        
    except Exception as e:
        st.error(f"❌ ایپ شروع کرنے میں خرابی: {str(e)}")
        logger.error(f"App startup error: {e}")
