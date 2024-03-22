from django.urls import path
from .views import VenueEvent

urlpatterns = [
    path('venue/<int:venue_id>/', VenueEvent.as_view(), name='venue-event'),
]