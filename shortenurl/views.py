from django.shortcuts import redirect, render

from .models import Url


def short_url_redirect(request, subpart):
    obj = Url.objects.get(subpart=subpart)
    return redirect(obj.long_url)


def front(request):
    return render(request, "index.html")
