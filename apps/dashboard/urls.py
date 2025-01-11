# Imports
from django.urls import path

from apps.dashboard import views as dashboard_views

# Set the app name
app_name = "dashboard"

# URL patterns
urlpatterns = [
    path("dashboard/", dashboard_views.home_view, name="home"),
    path(
        "api/playground/getPeriodIntervals/",
        dashboard_views.get_period_intervals_view,
        name="getPeriodIntervals",
    ),
    path(
        "<str:symbol>/playground/", dashboard_views.playground_view, name="playground"
    ),
]
