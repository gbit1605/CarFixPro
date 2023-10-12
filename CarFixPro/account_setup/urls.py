from django.urls import path
from . import views

urlpatterns = [
    path("landing_page", views.index),
    path("gun", views.test)
]