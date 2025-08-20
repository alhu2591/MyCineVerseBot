# -*- coding: utf-8 -*-
import json
import os
import logging

logger = logging.getLogger(__name__)
translations = {}

def load_translations():
    """يحمل كل ملفات اللغات من مجلد locales باستخدام مسار مطلق وآمن."""
    base_dir = os.path.abspath(os.path.dirname(__file__))
    locales_dir = os.path.join(base_dir, 'locales')
    
    if not os.path.exists(locales_dir):
        logger.error(f"Locales directory '{locales_dir}' not found.")
        return

    for filename in os.listdir(locales_dir):
        if filename.endswith('.json'):
            lang_code = filename.split('.')[0]
            try:
                with open(os.path.join(locales_dir, filename), 'r', encoding='utf-8') as f:
                    translations[lang_code] = json.load(f)
                    logger.info(f"Loaded language: {lang_code}")
            except Exception as e:
                logger.error(f"Failed to load language file {filename}: {e}")

def get_string(lang_code, key, **kwargs):
    """يجلب النص المترجم بناءً على لغة المستخدم والمفتاح."""
    lang_to_use = lang_code if lang_code in translations else 'en'
    
    keys = key.split('.')
    text = translations.get(lang_to_use, {})
    for k in keys:
        text = text.get(k)
        if text is None:
            return f"_{key}_"
    
    try:
        return text.format(**kwargs)
    except KeyError as e:
        logger.warning(f"Formatting key {e} not found for '{key}' in lang '{lang_to_use}'")
        return text
