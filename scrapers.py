# -*- coding: utf-8 -*-
import asyncio
import aiohttp
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import database

logger = logging.getLogger(__name__)
# ‼️ استخدام ترويسة متصفح حقيقي لمحاولة تجاوز الحظر
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}

async def fetch_html(session, url):
    """يجلب محتوى الصفحة بأمان."""
    try:
        async with session.get(url, headers=HEADERS, timeout=20, ssl=False) as response:
            response.raise_for_status()
            return await response.text()
    except Exception as e:
        logger.error(f"Failed to fetch {url}: {e}")
        return None

# --- دوال سحب البيانات لكل موقع ---

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

async def scrape_egybest(session):
    site_url = "https://i-egybest.com/"
    html = await fetch_html(session, site_url)
    items_list = []
    if not html: return 'EgyBest', items_list
    
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_='movie')
    for item in items:
        title = item.find('span', class_='title').text.strip()
        link = item['href']
        if title and link and not database.link_exists(link):
            items_list.append({'title': title, 'link': link, 'source': 'EgyBest'})
    return 'EgyBest', items_list

async def scrape_egydead(session):
    site_url = "https://tv2.egydead.live/"
    html = await fetch_html(session, site_url)
    items_list = []
    if not html: return 'EgyDead', items_list
    
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='MovieBlock')
    for item in items:
        link_tag = item.find('a', href=True)
        title = link_tag.get('title', '').strip()
        link = link_tag['href']
        if title and link and not database.link_exists(link):
            items_list.append({'title': title, 'link': link, 'source': 'EgyDead'})
    return 'EgyDead', items_list

async def scrape_tuktukcima(session):
    site_url = "https://tuktukcima.art/"
    html = await fetch_html(session, site_url)
    items_list = []
    if not html: return 'TukTukCima', items_list
    
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_='TPostMv')
    for item in items:
        title = item.find('h2', class_='Title').text.strip()
        link = item['href']
        if title and link and not database.link_exists(link):
            items_list.append({'title': title, 'link': link, 'source': 'TukTukCima'})
    return 'TukTukCima', items_list

async def scrape_cimaclub(session):
    site_url = "https://cimaclub.us/"
    html = await fetch_html(session, site_url)
    items_list = []
    if not html: return 'CimaClub', items_list
    
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.select('div.content-box ul.content-list li.item')
    for item in items:
        link_tag = item.find('a', href=True)
        title = item.find('h3').text.strip()
        link = urljoin(site_url, link_tag['href'])
        if title and link and not database.link_exists(link):
            items_list.append({'title': title, 'link': link, 'source': 'CimaClub'})
    return 'CimaClub', items_list

async def run_all_scrapers():
    """يشغل كل دوال السحب بشكل متزامن ويجمع النتائج."""
    logger.info("Running all scrapers...")
    all_new_items = []
    async with aiohttp.ClientSession() as session:
        # ‼️ أضف كل دوال السحب الخاصة بك هنا
        tasks = [
            scrape_wecima(session),
            scrape_egybest(session),
            scrape_egydead(session),
            scrape_tuktukcima(session),
            scrape_cimaclub(session)
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
