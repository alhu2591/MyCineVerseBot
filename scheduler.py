# -*- coding: utf-8 -*-
import logging
import asyncio
from telegram.ext import ContextTypes
import config, database, scrapers, tmdb_api, utils

logger = logging.getLogger(__name__)

async def check_updates(context: ContextTypes.DEFAULT_TYPE):
    """
    المهمة المجدولة التي تفحص المواقع وترسل التحديثات للقناة.
    """
    logger.info("Running scheduled job: Checking for new updates...")
    new_items = await scrapers.run_all_scrapers()
    
    if not new_items:
        logger.info("No new items found from any site.")
        return

    logger.info(f"Found a total of {len(new_items)} new items. Processing...")
    for item in reversed(new_items): # Reversed to post oldest first
        # Search TMDb to get the ID and type
        search_results = tmdb_api.search_media_by_title(item['title'])
        if not search_results:
            logger.warning(f"Could not find '{item['title']}' on TMDb. Skipping.")
            continue
        
        first_result = search_results[0]
        tmdb_id = first_result.id
        item_type = 'movie' if hasattr(first_result, 'title') else 'tv'
        
        # Get full details
        details = tmdb_api.get_details(tmdb_id, item_type, lang_code='ar')
        if not details:
            logger.warning(f"Could not get details for '{item['title']}'. Skipping.")
            continue

        # Build and send message
        message, keyboard = utils.build_message_and_buttons(
            details,
            watch_link=item['link'],
            source=item['source'],
            lang_code='ar'
        )
        
        try:
            if details.poster_path:
                poster_url = f"https://image.tmdb.org/t/p/w500{details.poster_path}"
                await context.bot.send_photo(
                    chat_id=config.CHANNEL_ID,
                    photo=poster_url,
                    caption=message,
                    parse_mode='Markdown',
                    reply_markup=keyboard
                )
            else:
                await context.bot.send_message(
                    chat_id=config.CHANNEL_ID,
                    text=message,
                    parse_mode='Markdown',
                    reply_markup=keyboard
                )
            
            # If successful, add the link to the database
            database.add_link(item['link'])
            logger.info(f"Successfully posted update for: {item['title']}")

        except Exception as e:
            logger.error(f"Failed to send update for {item['title']} to channel: {e}")
        
        await asyncio.sleep(5) # Delay between messages to avoid flooding
