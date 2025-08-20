# -*- coding: utf-8 -*-
import sqlite3
import logging

logger = logging.getLogger(__name__)
DB_NAME = 'bot_database_final.db'

def initialize_db():
    """ينشئ كل الجداول اللازمة عند بدء التشغيل."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY, 
            first_name TEXT, 
            language TEXT DEFAULT 'ar'
        )
    ''')
    cursor.execute('CREATE TABLE IF NOT EXISTS sent_items (link TEXT PRIMARY KEY)')
    conn.commit()
    conn.close()
    logger.info("Database initialized with scrapers support.")

def add_or_update_user(user_id, first_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id, first_name) VALUES (?, ?)", (user_id, first_name))
    conn.commit()
    conn.close()

def get_user_language(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT language FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    if not result:
        add_or_update_user(user_id, "User")
        return 'ar'
    return result[0]

def set_user_language(user_id, lang_code):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET language = ? WHERE user_id = ?", (lang_code, user_id))
    conn.commit()
    conn.close()

def link_exists(link):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM sent_items WHERE link = ?", (link,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def add_link(link):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO sent_items (link) VALUES (?)", (link,))
        conn.commit()
    except sqlite3.IntegrityError:
        logger.warning(f"Link {link} already exists in DB.")
    finally:
        conn.close()
