from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Event(models.Model):
  venue = models.ForeignKey('venues.Venue', on_delete=models.CASCADE, related_name='events_from_events_app')
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events_from_events_app')
  event = models.TextField()
  description = models.TextField()
  cost = models.TextField()
  duration = models.TextField()
  event_date = models.DateTimeField()
  time_start = models.DateTimeField()
  time_end = models.DateTimeField()
  category = models.TextField()
  photo = models.ImageField(upload_to='media/events')
  website = models.TextField()
  created_at = models.DateTimeField(default=timezone.now)


  def __str__(self):
    return f"Venue: {self.venue}, has the note: {self.event}"