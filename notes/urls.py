from django.urls import path
from .views import VenueNote

urlpatterns = [
    path('venue/<int:venue_id>/', VenueNote.as_view(), name='venue-note'),
]