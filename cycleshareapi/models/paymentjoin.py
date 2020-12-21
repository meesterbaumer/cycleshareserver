"""Model imports for PaymentJoin"""
from django.db import models
from . import Rider, Payment

class Paymentjoin(models.Model):
    """Model Class definition for PaymentJoin"""
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
