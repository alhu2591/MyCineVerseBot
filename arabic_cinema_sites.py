# arabic_cinema_sites.py

def get_free_arabic_sites():
    return [
        {"title": "wecima.click", "link": "https://wecima.click/", "type": "فيلم/مسلسل", "language": "عربي/مترجم"},
        {"title": "i-egybest.com", "link": "https://i-egybest.com/", "type": "فيلم/مسلسل", "language": "عربي/مترجم"},
        {"title": "tv2.egydead.live", "link": "https://tv2.egydead.live/", "type": "مسلسل", "language": "عربي"},
        {"title": "web6.topcinema.cam", "link": "https://web6.topcinema.cam/", "type": "فيلم/مسلسل", "language": "عربي/مترجم"},
        {"title": "tuktukcima.art", "link": "https://tuktukcima.art/", "type": "فيلم/مسلسل", "language": "عربي/مترجم"},
        {"title": "cimaclub.us", "link": "https://cimaclub.us/", "type": "فيلم/مسلسل", "language": "عربي/مترجم"},
    ]

def format_sites_list(sites):
    formatted = ""
    for s in sites:
        formatted += f"🎬 {s['title']} ({s['type']}, {s['language']})\n🔗 {s['link']}\n\n"
    return formatted
