from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favoured_venues = models.ManyToManyField('venues.Venue', related_name='favourited_by')

