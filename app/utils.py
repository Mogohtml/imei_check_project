import requests
import cachetools
import logging
from .config import API_TOKEN, WHITELIST, VALID_TOKENS

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

cache = cachetools.TTLCache(maxsize=100, ttl=3600)  # Кэш на 100 элементов с временем жизни 1 час

def check_imei(imei):
    if imei in cache:
        logger.info(f"Cache hit for IMEI {imei}")
        return cache[imei]

    url = "https://imeicheck.net/api/check-imei"
    params = {
        "imei": imei,
        "token": API_TOKEN
    }
    response = requests.post(url, data=params)
    result = response.json()
    cache[imei] = result
    logger.info(f"Cache miss for IMEI {imei}, result cached")
    return result

def is_user_allowed(user_id):
    return user_id in WHITELIST

def is_token_valid(token):
    return token in VALID_TOKENS
