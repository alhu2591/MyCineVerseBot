# -*- coding: utf-8 -*-
import logging
from tmdbv3api import TMDb, Movie, Search, TV, Discover
import config

logger = logging.getLogger(__name__)
tmdb = TMDb()
tmdb.api_key = config.TMDB_API_KEY

def discover_media(genre_id, keyword_id=None, lang_code='en'):
    """Finds media using the Discover endpoint."""
    discover = Discover()
    params = {
        'with_genres': str(genre_id),
        'sort_by': 'popularity.desc',
        'language': lang_code
    }
    if keyword_id:
        params['with_keywords'] = str(keyword_id)
        
    results = discover.discover_movies(params)
    return results

def get_details(tmdb_id, item_type, lang_code='en'):
    """Fetches full details for a movie or TV show."""
    try:
        tmdb.language = lang_code
        media = Movie() if item_type == 'movie' else TV()
        details = media.details(tmdb_id)
        return details
    except Exception as e:
        logger.error(f"Failed to get details for {tmdb_id}: {e}")
        return None
