from django.db import models

class Bikesize(models.Model):
	label = models.CharField(max_length=25)