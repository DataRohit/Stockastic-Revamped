# Imports
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

# Django admin urls
urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
]

# Health check urls
urlpatterns += [path("health/", include("health_check.urls"))]

# App urls
urlpatterns += [
    path("", include("apps.core.urls")),
]

# If the app is in debug mode
if settings.DEBUG:
    # Add Silk profiler urls
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]

# Admin configuration
admin.site.site_header = "Stockastic Admin"
admin.site.site_title = "Stockastic Admin"
admin.site.index_title = "Welcome to Stockastic Admin"
