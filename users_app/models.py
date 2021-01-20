from django.db import models
import re
from datetime import datetime

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=25, unique=True)
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    email = models.CharField(max_length=254, unique=True)
    dob = models.DateField()
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
