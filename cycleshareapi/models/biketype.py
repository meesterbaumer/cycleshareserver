from django.db import models

class Biketype(models.Model):
	label = models.CharField(max_length=25)