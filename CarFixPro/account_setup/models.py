from django.db import models
from passlib.hash import pbkdf2_sha256

# Create your models here.
class CustomerInfo(models.Model):
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    address = models.TextField()
    phone = models.CharField(max_length=10)
    email_id = models.EmailField()
    c_number = models.CharField(max_length=16)
    passwd = models.CharField(max_length=256, null=True)

    def verify_password(self, p):
        return pbkdf2_sha256.verify(p, self.passwd)

