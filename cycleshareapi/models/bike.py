"""Model imports for Bike"""
from django.db import models
from . import Bikesize, Biketype, Rider


class Bike(models.Model):
    """Model Class definition for Bike"""
    year = models.IntegerField()
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    image = models.ImageField(default='defaultbike.jpeg', upload_to='images/bikepics')
    fee = models.BooleanField()
    biketype = models.ForeignKey(Biketype, on_delete=models.CASCADE)
    bikesize = models.ForeignKey(Bikesize, on_delete=models.CASCADE)
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
