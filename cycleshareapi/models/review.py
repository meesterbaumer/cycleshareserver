"""Model imports for Review"""
from django.db import models
from . import Rider

class Review(models.Model):
    """Model Class definition for Bike"""
    message = models.CharField(max_length=500)
    author = models.ForeignKey(Rider, on_delete=models.CASCADE, related_name="reviewauthor")
    user = models.ForeignKey(Rider, on_delete=models.CASCADE, related_name="reviewdperson")
