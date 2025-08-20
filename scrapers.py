# -*- coding: utf-8 -*-
import asyncio
import aiohttp
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import database
import config # استيراد الإعدادات الجديدة

logger = logging.getLogger(__name__)

async def fetch_html(session, url):
    """
    يجلب محتوى الصفحة باستخدام خدمة Scraping API لتجاوز الحظر.
    """
    if not config.SCRAPER_API_KEY:
        logger.error("Scraper API Key is not configured.")
        return None
        
    # بناء رابط الطلب عبر الخدمة الوسيطة
    proxy_url = f'http://api.scraperapi.com?api_key={config.SCRAPER_API_KEY}&url={url}'
    
    try:
        async with session.get(proxy_url, timeout=60) as response: # زيادة مدة الانتظار
            response.raise_for_status()
            return await response.text()
    except Exception as e:
        logger.error(f"Failed to fetch {url} via ScraperAPI: {e}")
        return None

# --- دوال سحب البيانات لكل موقع (تبقى كما هي) ---

async def scrape_wecima(session):
    site_url = "https://wecima.click/"
    html = await fetch_html(session, site_url)
    items_list = []
    if not html: return 'WeCima', items_list
    
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='GridItem')
    for item in items:
        link_tag = item.find('a', href=True)
        title_tag = item.find('h3')
        if link_tag and title_tag:
            title = title_tag.text.strip()
            link = link_tag['href']
            if title and link and not database.link_exists(link):
                items_list.append({'title': title, 'link': link, 'source': 'WeCima'})
    return 'WeCima', items_list

# ... (بقية دوال السحب)

async def run_all_scrapers():
    """يشغل كل دوال السحب بشكل متزامن ويجمع النتائج."""
    logger.info("Running all scrapers via ScraperAPI...")
    all_new_items = []
    async with aiohttp.ClientSession() as session:
        tasks = [
            scrape_wecima(session),
            # ... (بقية المواقع)
        ] 
        results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for res in results:
        if isinstance(res, Exception):
            logger.error(f"A scraper task failed: {res}")
            continue
        site_name, items = res
        logger.info(f"Scraper '{site_name}' found {len(items)} new items.")
        all_new_items.extend(items)
    
    return all_new_items
