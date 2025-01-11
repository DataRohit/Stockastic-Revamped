# Imports
from django.urls import path

from apps.dashboard import views as dashboard_views

# Set the app name
app_name = "dashboard"

# URL patterns
urlpatterns = [
    path("", dashboard_views.home_view, name="home"),
    path("playground/", dashboard_views.playground_view, name="playground"),
]
