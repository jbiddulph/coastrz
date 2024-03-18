from rest_framework import serializers
from .models import Venue

class VenueSerializer(serializers.ModelSerializer):
  class Meta: 
    model = Venue
    fields = [
      'id', 
      'fsa_id',
      'venuename',
      'slug',
      'venuetype',
      'address',
      'address2',
      'town',
      'county',
      'postcode',
      'postalsearch',
      'telephone',
      'easting',
      'northing',
      'latitude',
      'longitude',
      'local_authority',
      'website',
      'photo',
      'is_live',
      'created_at',
      'updated_at'
    ]
