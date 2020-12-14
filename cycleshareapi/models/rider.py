from django.db import models
from django.contrib.auth.models import User
from . import State

class Rider(models.Model):
	user = models.OneToOneField(User, on_delete==models.CASCADE)
	address = models.CharField(max_length=75)
	city = models.CharField(max_length=50)
	image = models.ImageField(default='default.jpeg', upload_to='/images/profilePics')
	state = models.ForeignKey(State, on_delete=models.CASCADE)