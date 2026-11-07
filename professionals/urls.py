from django.urls import path
from . import views

app_name = "professionals"
urlpatterns = [path("", views.professionals, name="index")]
# La URL pública anterior sigue expuesta como core:professionals desde core/urls.py.
