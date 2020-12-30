"""Model imports for BikeType"""
from django.db import models

class Biketype(models.Model):
    """Model Class definition for BikeType"""
    label = models.CharField(max_length=25)

