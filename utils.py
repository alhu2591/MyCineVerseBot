# -*- coding: utf-8 -*-
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def build_message_and_buttons(details, watch_link=None, source=None, lang_code='ar'):
    """يبني الرسالة النهائية مع دعم روابط المشاهدة والمصدر."""
    title = details.title if hasattr(details, 'title') else details.name
    year = (details.release_date or details.first_air_date or "").split('-')[0]
    rating = round(details.vote_average, 1)
    overview = details.overview or "No overview available."
    genres = ', '.join([g['name'] for g in details.genres])

    message = f"**{title}** ({year})\n\n"
    message += f"⭐ **{rating}/10**\n"
    message += f"🎭 **{genres}**\n\n"
    message += f"📝 {overview}"

    if source:
        message += f"\n\n**المصدر:** {source}"

    buttons = []
    if watch_link:
        buttons.append([InlineKeyboardButton("🍿 شاهد الآن", url=watch_link)])
    
    if not watch_link: # For interactive journey
         buttons.append([InlineKeyboardButton("Back to Journey", callback_data="journey_start_over")])

    return message, InlineKeyboardMarkup(buttons) if buttons else None
