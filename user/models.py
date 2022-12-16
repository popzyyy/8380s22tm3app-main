from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    address = models.CharField(max_length=50, default=' ', null=True, blank=True)
    city = models.CharField(max_length=50, default=' ', null=True, blank=True)
    zipcode = models.CharField(max_length=5)

