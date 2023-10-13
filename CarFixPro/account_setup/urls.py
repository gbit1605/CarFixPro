from django.urls import path
from . import views

urlpatterns = [
    path("landing_page", views.index),
    path("thank-you", views.thank_you),
    path("customer_login", views.customer_login)
]