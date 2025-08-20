# -*- coding: utf-8 -*-
import os

# --- إعدادات تليجرام ---
# يقرأ التوكن من المتغيرات السرية في Render
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHANNEL_ID = '@MyCineVerse_bot'

# --- مفاتيح API ---
# يقرأ مفتاح TMDb من المتغيرات السرية في Render
TMDB_API_KEY = os.environ.get('TMDB_API_KEY')

# --- إعدادات المدير ---
# يقرأ ID المدير من المتغيرات السرية في Render
ADMIN_CHAT_ID = int(os.environ.get('ADMIN_CHAT_ID', 0))
