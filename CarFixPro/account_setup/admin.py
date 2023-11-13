from django.contrib import admin
from .models import CustomerInfo, Vehicle, Location, Service, Appointment, AppointmentStatus
# Register your models here.
admin.site.register(CustomerInfo)
admin.site.register(Vehicle)
admin.site.register(Location)
admin.site.register(Service)
admin.site.register(Appointment)
admin.site.register(AppointmentStatus)