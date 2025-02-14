"""URLs the whole application using"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import include, path
from django.views.generic.base import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("api.urls")),
    path("favicon.ico", RedirectView.as_view(url=staticfiles_storage.url("favicon.ico"))),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
