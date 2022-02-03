import logging

from django.core.cache import cache
from django.core.handlers.wsgi import WSGIRequest
from django.db import IntegrityError
from rest_framework.decorators import api_view  # type: ignore
from rest_framework.response import Response  # type: ignore

from shortenurl.models import Url

from .helpers import *
from .serializers import UrlSerializer

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


@api_view(["POST", "GET"])
def users_urls(request: WSGIRequest) -> Response:
    if request.method == "POST":
        long_url = request.POST.get("long")
        subpart_from_input = request.POST.get("subpart")
        short_url, subpart = generate_short_url(subpart_from_input)
        try:
            url_object = Url(long_url=long_url, short_url=short_url, subpart=subpart)
            url_object.save()
        except IntegrityError as e:
            return Response({"err": "subpart уже использовался, введите другой"})

        logger.info(f" Ссылка {short_url} добавлена в базу")
        add_url_to_session(request, short_url)
        cache_url(request, url_object)

        return Response(short_url)

    clear_session(request)
    # refresh_cache()
    urls = get_urls_from_cache(request)

    return Response(sorted(urls, key=lambda x: -x["id"]))
