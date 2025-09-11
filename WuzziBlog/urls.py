from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("posts.urls")),
    path("users/", include("users.urls")),   # all auth + register + reset live here
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("accounts/", include("django.contrib.auth.urls")),  # Re-added for auth URLs
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)