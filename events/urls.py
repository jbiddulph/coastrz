from django.urls import path
from .views import VenueEvent, Events

urlpatterns = [
    path('all/', Events.as_view(), name='events'),
    path('venue/<int:venue_id>/', VenueEvent.as_view(), name='venue-event'),
]