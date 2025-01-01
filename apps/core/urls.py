# Imports
from django.urls import path

from apps.core import views as core_views

# Set the app name
app_name = "core"

# URL patterns
urlpatterns = [
    path("", core_views.home_view, name="home"),
    path("dashboard/", core_views.dashboard_view, name="dashboard"),
]
