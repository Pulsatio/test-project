from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Company(models.Model):
    name = models.CharField(max_length=255)

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    representative = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class Interaction(models.Model):
    TYPES = [(t, t) for t in ["Call","Email","SMS","Facebook"]]
    customer = models.ForeignKey(Customer, related_name="interactions", on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPES)
    timestamp = models.DateTimeField()
    class Meta:
        ordering = ["-timestamp"]