# -*- coding: utf-8 -*-
import logging
from tmdbv3api import TMDb, Movie, Search, TV, Discover
import config

logger = logging.getLogger(__name__)
tmdb = TMDb()
tmdb.api_key = config.TMDB_API_KEY

def search_media_by_title(title, lang_code='ar'):
    """يبحث عن فيلم أو مسلسل بالاسم."""
    try:
        tmdb.language = lang_code
        search = Search()
        # Search for movies first, then TV shows
        results = search.search_movies(title)
        if not results:
            results = search.search_tv(title)
        return results
    except Exception as e:
        logger.error(f"Error searching for '{title}': {e}")
        return []

def discover_media(genre_id, keyword_id=None, lang_code='en'):
    discover = Discover()
    params = {'with_genres': str(genre_id), 'sort_by': 'popularity.desc', 'language': lang_code}
    if keyword_id:
        params['with_keywords'] = str(keyword_id)
    return discover.discover_movies(params)

def get_details(tmdb_id, item_type, lang_code='en'):
    try:
        tmdb.language = lang_code
        media = Movie() if item_type == 'movie' else TV()
        return media.details(tmdb_id)
    except Exception as e:
        logger.error(f"Failed to get details for {tmdb_id}: {e}")
        return None
