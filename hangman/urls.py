from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse


def no_favicon(request):
    return HttpResponse(status=204)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('favicon.ico', no_favicon),
    path("", include("game.urls")),
]
