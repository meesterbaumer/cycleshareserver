from django.db import models
from . import Rider, Payment

class Paymentjoin(models.Model):
	payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
	rider = models.ForeignKey(Rider, on_delete=models.CASCADE)