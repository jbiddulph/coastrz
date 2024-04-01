from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from venues.models import Venue
from .models import Event  # Import the Event model
from .serializers import EventSerializer
from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt

class Events(APIView):
    pagination_class = PageNumberPagination
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get(self, request):
        paginator = self.pagination_class()
        events = paginator.paginate_queryset(self.queryset, request)
        serializer = self.serializer_class(events, many=True)
        return paginator.get_paginated_response(serializer.data)
class VenueEvent(APIView):
  def get(self, request, venue_id):
        try:
            venue = Venue.objects.get(pk=venue_id)
        except Venue.DoesNotExist:
            return Response({"detail": "Venue not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Retrieve all notes for the specified venue
        events = Event.objects.filter(venue=venue)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

  def post(self, request, venue_id):
      try:
          venue = Venue.objects.get(pk=venue_id)
      except Venue.DoesNotExist:
          return Response({"detail": "Venue not found."}, status=status.HTTP_404_NOT_FOUND)
      
      # Extract user from request
      user = request.user
      
      # Combine request data with user
      request_data_with_user = request.data.copy()
      request_data_with_user['user'] = user.id
      
      # Create the serializer instance with the modified request data
      serializer = EventSerializer(data=request_data_with_user, partial=True)
      
      # Validate the serializer
      if serializer.is_valid():
          # Set the venue field to the venue object
          serializer.validated_data['venue'] = venue
          serializer.save()
          return Response(serializer.data, status=status.HTTP_201_CREATED)
      
      # Return serializer errors if validation fails
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)