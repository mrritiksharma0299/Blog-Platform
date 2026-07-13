from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.conf.urls.static import static

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from django.urls import path, include

from search import views as search_views

urlpatterns = [
    path("django-admin/", admin.site.urls),

    path("admin/", include(wagtailadmin_urls)),

    path("documents/", include(wagtaildocs_urls)),

    path("accounts/", include("accounts.urls")),

    path("search/", search_views.search, name="search"),

    path("blog/", include("blog.urls")),

    path("community/", include("community.urls")),

    path("", include("core.urls")),

    path("notifications/",include("notifications.urls")),
]


urlpatterns += [
    path("", include(wagtail_urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#     urlpatterns += staticfiles_urlpatterns()
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path("", include(wagtail_urls)),
]

