import logging
import os
import uuid
from random import randint
from typing import List, Tuple, Union, cast

from django.core.cache import cache
from dotenv import load_dotenv
from rest_framework.request import Request  # type: ignore

from shortenurl.models import Url

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
load_dotenv()

DOMAIN: str = cast(str, os.getenv("DOMAIN"))
CACHE_TTL: int = cast(int, int(os.getenv("CACHE_TTL")))  # type: ignore


def generate_short_url(subpart: Union[str, None] = None) -> Tuple[str, str]:
    """Генерация короткой ссылки"""
    subpart = subpart or str(uuid.uuid4())[:6]
    return (DOMAIN + subpart, subpart)


def add_url_to_session(request: Request, short_url: str) -> None:
    """Добавление короткой ссылки в объект сессии"""
    if "users_urls" in request.session:
        request.session["users_urls"].append(short_url)
        request.session.save()
    else:
        request.session["users_urls"] = [short_url]
        request.session.save()
    logger.info(f" Ссылка {short_url} добавлена в сессию {request.session.session_key}")


def update_current_cache(request: Request, url: Url) -> None:
    """Занесение в кеш переданной ссылки"""
    current_cache = cache.get(request.session.session_key)
    current_cache.append(
        {"long_url": url.long_url, "short_url": url.short_url, "id": url.id}
    )
    cache.set(request.session.session_key, current_cache, CACHE_TTL)


def cache_url(request: Request, url: Url) -> None:
    """Обновление или инициализация кеша. Кеширование ссылки."""
    if not (cache.get(request.session.session_key)):
        cache.set(
            request.session.session_key,
            [{"long_url": url.long_url, "short_url": url.short_url, "id": url.id}],
            CACHE_TTL,
        )
        logger.info(f" Кеш создан")
    else:
        update_current_cache(request, url)
        logger.info(f" Кеш обновлен")
    logger.info(f" {url.short_url} добавлена в кеш")


def clear_session(request: Request) -> None:
    """Очистка сессии"""
    cached_urls = cache.get(request.session.session_key)
    if "users_urls" in request.session and cached_urls:
        for url in request.session["users_urls"]:
            if url not in cached_urls:
                request.session["users_urls"].remove(url)
                request.session.modified = True
        logger.info(" Сессия очищена от просроченных ссылок")


def get_urls_from_cache(request: Request) -> list:
    """Получение ссылки из кеша и приведение к нужной структуре"""
    urls = []
    if cache.get(request.session.session_key):
        cached_urls = cache.get(request.session.session_key)
        for url in cached_urls:
            urls.append(
                {
                    "long_url": url["long_url"],
                    "short_url": url["short_url"],
                    "id": url["id"],
                }
            )
    logger.info(f" Получено {len(urls)} ссылок из кеша")
    return urls
