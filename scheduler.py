# -*- coding: utf-8 -*-
import logging
import asyncio
from telegram.ext import ContextTypes
import config, database, scrapers, tmdb_api, utils

logger = logging.getLogger(__name__)

async def check_updates(context: ContextTypes.DEFAULT_TYPE):
    """المهمة المجدولة التي تفحص المواقع وترسل التحديثات للقناة."""
    job_name = context.job.name if context.job else 'manual'
    logger.info(f"Running job '{job_name}': Checking for new updates...")
    new_items = await scrapers.run_all_scrapers()
    
    if not new_items:
        logger.info("No new items found from any site.")
        if job_name == 'force_check':
            await context.bot.send_message(chat_id=config.ADMIN_CHAT_ID, text="✅ الفحص اليدوي اكتمل. لم يتم العثور على أي إضافات جديدة.")
        return

    if job_name == 'force_check':
        await context.bot.send_message(chat_id=config.ADMIN_CHAT_ID, text=f"🔎 تم العثور على {len(new_items)} إضافة جديدة. جار النشر...")

    for item in reversed(new_items):
        search_results = tmdb_api.search_media_by_title(item['title'])
        if not search_results: continue
        
        first_result = search_results[0]
        tmdb_id = first_result.id
        item_type = 'movie' if hasattr(first_result, 'title') else 'tv'
        
        details = tmdb_api.get_details(tmdb_id, item_type, lang_code='ar')
        if not details: continue

        message, keyboard = utils.build_message_and_buttons(
            details, watch_link=item['link'], source=item['source'], lang_code='ar'
        )
        
        try:
            if details.poster_path:
                poster_url = f"https://image.tmdb.org/t/p/w500{details.poster_path}"
                await context.bot.send_photo(
                    chat_id=config.CHANNEL_ID, photo=poster_url, caption=message,
                    parse_mode='Markdown', reply_markup=keyboard
                )
            else:
                await context.bot.send_message(
                    chat_id=config.CHANNEL_ID, text=message,
                    parse_mode='Markdown', reply_markup=keyboard
                )
            
            database.add_link(item['link'])
            logger.info(f"Successfully posted update for: {item['title']}")

        except Exception as e:
            logger.error(f"Failed to send update for {item['title']} to channel: {e}")
        
        await asyncio.sleep(5)
