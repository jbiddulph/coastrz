from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes_from_notes_app')
    venue = models.ForeignKey('venues.Venue', on_delete=models.CASCADE, related_name='notes_from_notes_app')  
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Venue: {self.venue}, has the note: {self.text}"