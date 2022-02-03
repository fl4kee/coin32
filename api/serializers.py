from rest_framework import serializers  # type: ignore

from shortenurl.models import Url


class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = "__all__"
