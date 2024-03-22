from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'venue', 'user', 'event', 'description', 'cost', 'duration', 'event_date', 'time_start', 'time_end', 'category', 'photo', 'website', 'created_at']