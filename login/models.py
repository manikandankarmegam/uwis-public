from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Define different user roles using choices

    ROLE_CHOICES = [
        ('Admin', 'Admin'),  # value, display
        ('Qc', 'Qc'),
        ('Cliet', 'Client'),

    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=True, blank=True)




