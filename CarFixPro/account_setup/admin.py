from django.contrib import admin
from .models import CustomerInfo, Vehicle, Location, Service

# Register your models here.
admin.site.register(CustomerInfo)
admin.site.register(Vehicle)
admin.site.register(Location)
admin.site.register(Service)
