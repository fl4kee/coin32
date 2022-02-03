from django.urls import include, path

from . import views

urlpatterns = [
    path("<str:subpart>/", views.short_url_redirect),
    path("api/", include("api.urls")),
    path("", views.front, name="front"),
]
