from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from venues.models import Venue
from .serializers import NoteSerializer
from django.conf import settings
from rest_framework.permissions import AllowAny
# Create your views here.
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
class VenueNote(APIView):
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
        serializer = NoteSerializer(data=request_data_with_user)
        
        # Validate the serializer
        if serializer.is_valid():
            # Set the venue field to the venue object
            serializer.validated_data['venue'] = venue
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Return serializer errors if validation fails
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
