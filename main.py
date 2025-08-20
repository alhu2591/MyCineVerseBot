# -*- coding: utf-8 -*-
import logging
import config, database, localization
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
)
from interactive_journeys import (
    start_journey, handle_mood, handle_path, handle_refinement, cancel_journey,
    MOOD, PATH, REFINE
)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = database.get_user_language(user_id)
    database.add_or_update_user(user_id, update.effective_user.first_name)
    await update.message.reply_text(localization.get_string(lang, "welcome_message"))

async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = database.get_user_language(user_id)
    text = localization.get_string(lang, "language_select")
    buttons = [
        [
            InlineKeyboardButton("العربية 🇸🇦", callback_data="set_lang_ar"),
            InlineKeyboardButton("English 🇬🇧", callback_data="set_lang_en"),
        ]
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))

async def handle_language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang_code = query.data.split('_')[-1]
    database.set_user_language(user_id, lang_code)
    text = localization.get_string(lang_code, "language_changed")
    await query.edit_message_text(text)

def main():
    if 'ضع' in config.TELEGRAM_TOKEN or 'ضع' in config.TMDB_API_KEY:
        logger.error("‼️ خطأ: الرجاء تعبئة الإعدادات في ملف config.py"); return
    
    localization.load_translations()
    database.initialize_db()
    
    app = Application.builder().token(config.TELEGRAM_TOKEN).build()

    journey_handler = ConversationHandler(
        entry_points=[CommandHandler('journey', start_journey)],
        states={
            MOOD: [CallbackQueryHandler(handle_mood, pattern='^journey_mood_')],
            PATH: [CallbackQueryHandler(handle_path, pattern='^journey_path_')],
            REFINE: [CallbackQueryHandler(handle_refinement, pattern='^journey_refine_')],
        },
        fallbacks=[
            CommandHandler('cancel', cancel_journey),
            CallbackQueryHandler(start_journey, pattern='^journey_start_over$')
        ]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("language", language_command))
    app.add_handler(journey_handler)
    app.add_handler(CallbackQueryHandler(handle_language_callback, pattern='^set_lang_'))

    logger.info("Bot is running..."); app.run_polling()

if __name__ == '__main__':
    main()
