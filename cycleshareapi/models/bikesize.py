"""Model imports for BikeSize"""
from django.db import models


class Bikesize(models.Model):
    """Model Class definition for BikeSize"""
    label = models.CharField(max_length=25)
