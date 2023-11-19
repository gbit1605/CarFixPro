from django.urls import path
from . import views

urlpatterns = [
    path("landing_page", views.index),
    path("thank-you", views.thank_you),
    path("customer_login", views.customer_login),
    path("manager_login", views.manager_login),
    path("technician_login", views.technician_login),
    path("technician_dashboard", views.technician_dashboard),
    path("customer_dashboard", views.customer_dashboard),
    path("manager_dashboard", views.manager_dashboard),
    path("manager_pending_approvals", views.manager_pending_approvals, name="manager_pending_approvals"),
    path("technician_pending_appointments", views.technician_pending_appointments, name="technician_pending_appointments"),
    path("book_appointment", views.book_appointment, name="book_appointment"),
    path("add_vehicle", views.add_vehicle, name="add_vehicle"), 
    path("technician_registration", views.technician_registration, name="technician_registration"),
    path("add_technician_skills", views.add_technician_skills, name="add_technician_skills"),
    path("delete_technician_skills", views.delete_technician_skills, name="delete_technician_skills"),
    path("add_technician_skills/<str:test_number>", views.add_technician_skills_choices, name="add_technician_skills_choices"),
    path("delete_technician_skills/<str:test_number>", views.delete_technician_skills_choices, name="delete_technician_skills_choices"),
    path("manager_appointment_finish_approval", views.manager_appointment_finish_approval, name="manager_appointment_finish_approval")
]