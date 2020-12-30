"""Model imports for reservations"""
from django.db import models
from . import Rider, Bike, Payment

class Reservation(models.Model):
    """Model Class definition for reservations"""
    date = models.DateField(auto_now=False, auto_now_add=False)
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
