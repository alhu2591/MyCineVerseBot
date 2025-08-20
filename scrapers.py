# -*- coding: utf-8 -*-
import asyncio
import aiohttp
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import database

logger = logging.getLogger(__name__)
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

async def fetch_html(session, url):
    try:
        async with session.get(url, headers=HEADERS, timeout=20) as response:
            response.raise_for_status()
            return await response.text()
    except Exception as e:
        logger.error(f"Failed to fetch {url}: {e}")
        return None

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

# --- يمكنك إضافة دوال سحب لبقية المواقع هنا بنفس النمط ---
# async def scrape_egybest(session): ...

async def run_all_scrapers():
    logger.info("Running all scrapers...")
    all_new_items = []
    async with aiohttp.ClientSession() as session:
        # ‼️ أضف كل دوال السحب الخاصة بك هنا
        tasks = [scrape_wecima(session)] 
        results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for res in results:
        if isinstance(res, Exception):
            logger.error(f"A scraper task failed: {res}")
            continue
        site_name, items = res
        logger.info(f"Scraper '{site_name}' found {len(items)} new items.")
        all_new_items.extend(items)
    
    return all_new_items
