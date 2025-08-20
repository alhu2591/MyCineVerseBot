# -*- coding: utf-8 -*-
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def build_message_and_buttons(details, lang_code='ar'):
    """Builds the final message and buttons with full details."""
    title = details.title if hasattr(details, 'title') else details.name
    year = (details.release_date or details.first_air_date or "").split('-')[0]
    rating = round(details.vote_average, 1)
    overview = details.overview or "No overview available."
    genres = ', '.join([g['name'] for g in details.genres])

    message = f"**{title}** ({year})\n\n"
    message += f"⭐ **{rating}/10**\n"
    message += f"🎭 **{genres}**\n\n"
    message += f"📝 {overview}"

    # In a real scenario, you'd add like/subscribe buttons etc. here
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Back to Journey", callback_data="journey_start_over")]])
    
    return message, keyboard
