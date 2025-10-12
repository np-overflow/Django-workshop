from django.urls import path
from . import views

app_name = "url_shortener"  # Changed from 'shortener' to match your app name

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:alias>/", views.redirect_to_original, name="redirect"),
]
