from django.urls import path
from . import views

urlpatterns = [
    path("landing_page", views.index),
    path("thank-you", views.thank_you),
    path("customer_login", views.customer_login),
    path("customer_dashboard", views.customer_dashboard),
    path("book_appointment", views.book_appointment, name="book_appointment"),
    path("add_vehicle", views.add_vehicle, name="add_vehicle")
]