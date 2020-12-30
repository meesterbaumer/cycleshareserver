"""Model imports for Payments"""
from django.db import models

class Payment(models.Model):
    """Model Class definition for Payments"""
    name = models.CharField(max_length=25)
