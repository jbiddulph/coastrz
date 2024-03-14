from rest_framework import serializers
from django.contrib.auth.models import User
from venues.models import Venue

class UserSerializer(serializers.ModelSerializer):
  class Meta(object):
    model = User
    fields = ['id', 'username', 'password', 'email']

class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ['fsa_id', 'venuename', 'slug', 'venuetype', 'address', 'address2', 'town', 'county', 'postcode', 'postalsearch', 'telephone', 'easting', 'northing', 'latitude', 'longitude', 'local_authority', 'website', 'photo', 'is_live', 'created_at', 'updated_at']