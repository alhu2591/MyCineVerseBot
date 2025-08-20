# -*- coding: utf-8 -*-
import os

# --- إعدادات تليجرام ---
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHANNEL_ID = '@MyCineVerse_bot'

# --- مفاتيح API ---
TMDB_API_KEY = os.environ.get('TMDB_API_KEY')
# ‼️ المفتاح الجديد للخدمة الوسيطة
SCRAPER_API_KEY = os.environ.get('SCRAPER_API_KEY')

# --- إعدادات المدير ---
ADMIN_CHAT_ID = int(os.environ.get('ADMIN_CHAT_ID', 0))
