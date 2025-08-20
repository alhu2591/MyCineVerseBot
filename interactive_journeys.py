# -*- coding: utf-8 -*-
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
import localization, tmdb_api, utils, database

# تعريف состояний المحادثة
MOOD, PATH, REFINE, RESULT = range(4)

# هيكل الرحلة (منطق فقط، بدون نصوص)
journey_structure = {
    'moods': {
        'adventure': {
            'paths': {
                'galaxy': { 'refinements': { 'epic': {'genre_id': 878}, 'horror': {'genre_id': 27} }},
                'jungle': { 'refinements': { 'treasure': {'genre_id': 12}, 'survival': {'genre_id': 53} }}
            }
        },
        'laugh': {
            'paths': {
                'social': { 'refinements': { 'satire': {'genre_id': 35, 'keyword': 191414}, 'romcom': {'genre_id': 10749} }},
                'absurd': { 'refinements': { 'dark': {'genre_id': 35, 'keyword': 225538}, 'slapstick': {'genre_id': 35, 'keyword': 9715} }}
            }
        }
    }
}

async def start_journey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """يبدأ رحلة سينمائية جديدة بلغة المستخدم."""
    user_id = update.effective_user.id
    lang = database.get_user_language(user_id)
    context.user_data['lang'] = lang # Store lang for the conversation
    
    prompt = localization.get_string(lang, "journey.mood_prompt")
    
    buttons = [
        [InlineKeyboardButton(localization.get_string(lang, f"journey.moods.{mood_key}.label"), callback_data=f"journey_mood_{mood_key}")]
        for mood_key in journey_structure['moods'].keys()
    ]
    
    # Check if called from a query or a command
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(prompt, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await update.message.reply_text(prompt, reply_markup=InlineKeyboardMarkup(buttons))
        
    return MOOD

async def handle_mood(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """يتعامل مع اختيار المزاج."""
    query = update.callback_query
    await query.answer()
    
    lang = context.user_data.get('lang', 'ar')
    mood = query.data.split('_')[-1]
    context.user_data['journey_mood'] = mood
    
    prompt = localization.get_string(lang, f"journey.moods.{mood}.prompt")
    
    buttons = [
        [InlineKeyboardButton(localization.get_string(lang, f"journey.moods.{mood}.paths.{path_key}.label"), callback_data=f"journey_path_{path_key}")]
        for path_key in journey_structure['moods'][mood]['paths'].keys()
    ]
    await query.edit_message_text(text=prompt, reply_markup=InlineKeyboardMarkup(buttons))
    return PATH

async def handle_path(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """يتعامل مع اختيار المسار."""
    query = update.callback_query
    await query.answer()

    lang = context.user_data.get('lang', 'ar')
    path = query.data.split('_')[-1]
    mood = context.user_data['journey_mood']
    context.user_data['journey_path'] = path

    prompt = localization.get_string(lang, f"journey.moods.{mood}.paths.{path}.prompt")
    
    buttons = [
        [InlineKeyboardButton(localization.get_string(lang, f"journey.moods.{mood}.paths.{path}.refinements.{refine_key}.label"), callback_data=f"journey_refine_{refine_key}")]
        for refine_key in journey_structure['moods'][mood]['paths'][path]['refinements'].keys()
    ]
    await query.edit_message_text(text=prompt, reply_markup=InlineKeyboardMarkup(buttons))
    return REFINE

async def handle_refinement(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """يتعامل مع التنقيح النهائي ويعرض النتيجة."""
    query = update.callback_query
    await query.answer()

    lang = context.user_data.get('lang', 'ar')
    refinement = query.data.split('_')[-1]
    mood = context.user_data['journey_mood']
    path = context.user_data['journey_path']
    
    refinement_data = journey_structure['moods'][mood]['paths'][path]['refinements'][refinement]
    genre_id = refinement_data.get('genre_id')
    keyword_id = refinement_data.get('keyword')
    
    await query.edit_message_text(text=localization.get_string(lang, "journey.finding_result"))
    
    # استخدام TMDb Discover API للعثور على فيلم يطابق التصنيف
    results = tmdb_api.discover_media(genre_id, keyword_id, lang_code=lang)
    
    if results:
        details = tmdb_api.get_details(results[0].id, 'movie', lang_code=lang)
        if details:
            message, keyboard = utils.build_message_and_buttons(details, lang_code=lang)
            if details.poster_path:
                poster_url = f"https://image.tmdb.org/t/p/w500{details.poster_path}"
                await context.bot.send_photo(chat_id=query.message.chat_id, photo=poster_url, caption=message, parse_mode='Markdown', reply_markup=keyboard)
            else:
                await context.bot.send_message(chat_id=query.message.chat_id, text=message, parse_mode='Markdown', reply_markup=keyboard)
    else:
        await context.bot.send_message(chat_id=query.message.chat_id, text=localization.get_string(lang, "journey.no_result"))

    # تنظيف بيانات الرحلة
    context.user_data.pop('journey_mood', None)
    context.user_data.pop('journey_path', None)
    
    return ConversationHandler.END

async def cancel_journey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """يلغي الرحلة الحالية."""
    lang = database.get_user_language(update.effective_user.id)
    await update.message.reply_text(localization.get_string(lang, "journey.cancelled"))
    return ConversationHandler.END
