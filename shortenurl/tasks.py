import logging

from django.core.cache import cache

from core.celery import celery_app
from shortenurl.models import Url

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


@celery_app.task(bind=True, queue="clearing_database")
def say_hello(self):
    cached_urls = []
    cache_keys = cache.keys("*")
    for key in cache_keys:
        cached_urls += cache.get(key)
    cached_urls = [url["short_url"] for url in cached_urls]
    logger.info(f" Закешированные ссылки: {cached_urls}")
    urls = Url.objects.all()
    for url in urls:
        if not (url.short_url in cached_urls):
            Url.objects.get(short_url=url.short_url).delete()
