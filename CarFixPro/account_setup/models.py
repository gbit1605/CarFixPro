from django.db import models
from passlib.hash import pbkdf2_sha256
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
import re

# Create your models here.
class CustomerInfo(models.Model):

    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    address = models.TextField()
    phone = models.CharField(max_length=10)
    email_id = models.EmailField(primary_key=True, null=False)
    c_number = models.CharField(max_length=16)
    passwd = models.CharField(max_length=256, null=True)

    def verify_password(self, p):
        return pbkdf2_sha256.verify(p, self.passwd)

class Vehicle(models.Model):

    def validate_capital_or_digit(value):
        if not any(char.isupper() or char.isdigit() for char in value):
            raise ValidationError(
                'The value must contain at least one capital letter or digit.',
                code='invalid_capital_or_digit',)
        
    CHOICES  = (('Sedan', 'Sedan'), ('SUV', 'SUV'), ('Hatchback', 'Hatchback'), ('Crossover', 'Crossover'))

    customer_email = models.ForeignKey(CustomerInfo, on_delete=models.CASCADE)
    vin = models.CharField(max_length=17, primary_key=True, validators=[validate_capital_or_digit, MinLengthValidator(17), MaxLengthValidator(17)])
    model = models.CharField(max_length=50)
    year = models.CharField(max_length=4, validators=[MinLengthValidator(4), MaxLengthValidator(4)])
    color = models.CharField(max_length=10)
    mfg_company = models.CharField(max_length=20)
    vtype = models.CharField(max_length=10, choices=CHOICES, null=False)

class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=30)
    state = models.CharField(max_length=2)
    pincode = models.CharField(max_length=5)

class Service(models.Model):

    CHOICES_SERVICES  = (('Maintenance and Repairs', 'Maintenance and Repairs'), 
                        ('Diagnostic Services', 'Diagnostic Services'), 
                        ('Body and Paint Services', 'Body and Paint Services'), 
                        ('Detailing Services', 'Detailing Services'), 
                        ('Customization Services', 'Customization Services'), 
                        ('Towing and Recovery Services', 'Towing and Recovery Services'), 
                        ('Pre-Purchase Inspection', 'Pre-Purchase Inspection'),
                        ('Rental and Leasing Services', 'Rental and Leasing Services'),
                        ('Consultation and Advice', 'Consultation and Advice'))
    
    CHOICES_VTYPE  = (('Sedan', 'Sedan'), ('SUV', 'SUV'), ('Hatchback', 'Hatchback'), ('Crossover', 'Crossover'))
    
    service_type = models.CharField(max_length=30, choices=CHOICES_SERVICES)
    vehicle_type = models.CharField(max_length=30, choices=CHOICES_VTYPE)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['service_type', 'vehicle_type'], name='composite_pk')
        ]


class Appointment(models.Model):

    appointment_id = models.AutoField(primary_key=True)
    date = models.DateField()
    vehicle_id = models.CharField(max_length=17)
    vehicletype = models.CharField(max_length=30)  
    customer_email = models.ForeignKey(CustomerInfo, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    service_details = models.CharField(max_length=250)
    total_price = models.DecimalField(decimal_places=2, max_digits=8)

