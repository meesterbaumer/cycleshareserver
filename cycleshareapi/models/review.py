from django.db import models
from . import Rider

class Review(models.Model):
	message = models.CharField(max_length=500)
	author = models.ForeignKey(Rider, on_delete=models.CASCADE)
	user = models.ForeignKey(Rider, on_delete=models.CASCADE)