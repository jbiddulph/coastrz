from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import UserSerializer, VenueSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404

@api_view(["POST"])
def login(request):
  user = get_object_or_404(User, username=request.data['username'])
  if not user.check_password(request.data['password']):
    return Response({"detail": "Not found" }, status=status.HTTP_404_NOT_FOUND)
  token, created = Token.objects.get_or_create(user=user)
  serializer = UserSerializer(instance=user)
  return Response({"token": token.key, "user": serializer.data})

@api_view(["POST"])
def signup(request):
  serializer = UserSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save()
    user = User.objects.get(username=request.data['username'])
    user.set_password(request.data['password'])
    user.save()
    token = Token.objects.create(user=user)
    return Response({"token": token.key, "user": serializer.data})  
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user(request):
  user = request.user
  # Retrieve the user's ID, email, and username
  user_id = user.id
  email = user.email
  username = user.username
  # Construct a dictionary with the user information
  user_info = {
      'id': user_id,
      'email': email,
      'username': username
  }
  return Response(user_info)

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    # Get the user's authentication token
    token = request.auth

    # If token exists, delete it
    if token:
        token.delete()
        return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
    else:
        # If no token is found, return an error response
        return Response({"detail": "Invalid token or user not logged in"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def FavouredVenuesAPIView(request):
    user = request.user
    if user.is_authenticated:
      favoured_venues = user.favoured_venues.all()
      serializer = VenueSerializer(favoured_venues, many=True)
      return Response(serializer.data)
    else:
        # Handle case when user is not authenticated
        return Response({"message": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)