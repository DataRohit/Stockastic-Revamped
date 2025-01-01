# Imports
from django.urls import path

from apps.account import views as account_views

# Set the app name
app_name = "account"

# URL patterns
urlpatterns = [
    path("login/", account_views.login_view, name="login"),
    path("logout/", account_views.logout_view, name="logout"),
    path("register/", account_views.register_view, name="register"),
    path("profile/", account_views.profile_view, name="profile"),
]
