import logging
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.http import JsonResponse
from .models import Venue
from .serializers import VenueSerializer
from django.core.serializers import serialize
from django.contrib.gis.db.models.functions import AsGeoJSON
from django.contrib.gis.serializers.geojson import Serializer as GeoJSONSerializer
import os
from django.conf import settings
from django.db.models import F
from django.db.models import Count
from rest_framework.permissions import AllowAny
logger = logging.getLogger(__name__)

class VenueListView(APIView):
    pagination_class = PageNumberPagination
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer

    def get(self, request):
        paginator = self.pagination_class()
        venues = paginator.paginate_queryset(self.queryset, request)
        serializer = self.serializer_class(venues, many=True)
        return paginator.get_paginated_response(serializer.data)

class VenueGEOJsonListView(APIView):
    def get(self, request):
        venues = Venue.objects.annotate(geojson=AsGeoJSON('geometry'))
        geojson_data = serialize('geojson', venues, geometry_field='geojson')
        return JsonResponse(geojson_data, safe=False)
  
class VenueAdd(APIView): 
  def post(self, request):
      logger.debug("Request data: %s", request.data)
      serializer = VenueSerializer(data=request.data, partial=True)  # Allow partial updates
      if serializer.is_valid():
          serializer.save()
          return JsonResponse({'message': 'Venue created successfully'}, status=status.HTTP_201_CREATED)
      else:
          return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def post(self, request):
        serializer = VenueSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # Handle file upload
            if 'photo' in request.FILES:
                photo = request.FILES['photo']
                filename = photo.name
                # Save the file to the specified directory
                with open(os.path.join(settings.MEDIA_ROOT, 'photos', filename), 'wb') as f:
                    for chunk in photo.chunks():
                        f.write(chunk)
                # Update the venue object with the photo URL
                venue = serializer.instance
                venue.photo = os.path.join(settings.MEDIA_URL, 'photos', filename)
                venue.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VenueFSA(APIView):
    def get(self, request, fsa_id):
        try:
            venue = Venue.objects.get(fsa_id=fsa_id)
            serializer = VenueSerializer(venue)
            return Response(serializer.data)
        except Venue.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class VenueDetail(APIView):
  def get(self, request, id):
    try:
      venue = Venue.objects.get(pk=id)
    except Venue.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = VenueSerializer(venue)
    return Response(serializer.data)
  def put(self, request, id):
    try:
      venue = Venue.objects.get(pk=id)
    except Venue.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = VenueSerializer(venue,data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  def delete(self, request, id):
    try:
      venue = Venue.objects.get(pk=id)
    except Venue.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)
    venue.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
  
class VenueTowns(APIView):
  def get(self, request):
      try:
          venues = Venue.objects.all()
          # Extract distinct towns from venues
          distinct_towns = venues \
                .values_list('town', flat=True) \
                .distinct() \
                .exclude(town__regex=r'^\d+\s') \
                .exclude(town__startswith='The ') \
                .exclude(town__endswith=' Road') \
                .exclude(town__endswith=' Street') \
                .exclude(town__endswith=' Terrace') \
                .exclude(town__endswith=' Row') \
                .exclude(town__endswith=' Square') \
                .exclude(town__endswith=' Lane') \
                .exclude(town__endswith=' Place') \
                .exclude(town__endswith=' Drive') \
                .exclude(town__endswith=' Hill') \
                .exclude(town__endswith=' Green') \
                .exclude(town__endswith=' Park') \
                .exclude(town__regex=r'^\d{2}[a-zA-Z]') \
                .exclude(town__regex=r'^\d+\s') \
                .exclude(town__regex=r'\d+-\d+') \
                .exclude(town__regex=r'\d+') \
                .exclude(town__regex=r'^\w+( \w+){3,}') \
                .exclude(town__regex=r'[&]') \
                .exclude(town__regex=r'[\]')

          # Return distinct towns as response
          return Response({"towns": list(distinct_towns)})
      except Exception as e:
          return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      
class VenueCounties(APIView):
  def get(self, request):
        # Apply filters to get distinct towns
        filtered_counties = Venue.objects \
            .values_list('county', flat=True) \
            .distinct() \
            .exclude(county__regex=r'^\d+\s') \
            .exclude(county__startswith='The ') \
            .exclude(county__startswith='NN') \
            .exclude(county__endswith=' Road') \
            .exclude(county__endswith=' Street') \
            .exclude(county__endswith=' Terrace') \
            .exclude(county__endswith=' Row') \
            .exclude(county__endswith=' Square') \
            .exclude(county__endswith=' Lane') \
            .exclude(county__endswith=' Place') \
            .exclude(county__endswith=' Drive') \
            .exclude(county__endswith=' Hill') \
            .exclude(county__regex=r'^\d{2}[a-zA-Z]') \
            .exclude(county__regex=r'^\d+\s') \
            .exclude(county__regex=r'\d+-\d+') \
            .exclude(county__regex=r'\d+') \
            .exclude(county__regex=r'^\w+( \w+){3,}')

        # Query venues count per filtered county
        venues_count_by_county = Venue.objects \
            .filter(county__in=filtered_counties) \
            .values('county') \
            .annotate(venue_count=Count('id'))

        # Create a list of JSON objects with county and venue count
        counties_and_venues = []
        for item in venues_count_by_county:
            county = item['county']
            venue_count = item['venue_count']
            county_venue = {'county': county, 'count': venue_count}
            counties_and_venues.append(county_venue)

        # Return the JSON response
        return JsonResponse(counties_and_venues, safe=False)
      
class VenueTowns(APIView):
  def get(self, request):
        # Apply filters to get distinct towns
        filtered_towns = Venue.objects \
            .values_list('town', flat=True) \
            .distinct() \
            .exclude(town__regex=r'^\d+\s') \
            .exclude(town__startswith='The ') \
            .exclude(town__endswith=' Road') \
            .exclude(town__endswith=' Street') \
            .exclude(town__endswith=' Terrace') \
            .exclude(town__endswith=' Row') \
            .exclude(town__endswith=' Square') \
            .exclude(town__endswith=' Lane') \
            .exclude(town__endswith=' Place') \
            .exclude(town__endswith=' Drive') \
            .exclude(town__endswith=' Hill') \
            .exclude(town__regex=r'^\d{2}[a-zA-Z]') \
            .exclude(town__regex=r'^\d+\s') \
            .exclude(town__regex=r'\d+-\d+') \
            .exclude(town__regex=r'\d+') \
            .exclude(town__regex=r'^\w+( \w+){3,}')

        # Query venues count per filtered town
        venues_count_by_town = Venue.objects \
            .filter(town__in=filtered_towns) \
            .values('town') \
            .annotate(venue_count=Count('id'))

        # Create a list of JSON objects with town and venue count
        towns_and_venues = []
        for item in venues_count_by_town:
            town = item['town']
            venue_count = item['venue_count']
            town_venue = {'town': town, 'count': venue_count}
            towns_and_venues.append(town_venue)

        return JsonResponse(towns_and_venues, safe=False)
  
class VenueNames(APIView):
    pagination_class = PageNumberPagination

    def get(self, request):
        paginator = self.pagination_class()
        venues = Venue.objects.all()

        # Extract distinct venuename from venues
        filtered_names = venues \
              .values_list('venuename', flat=True) \
              .distinct() \
              # .exclude(venuename__regex=r'^\d+\s') \
              # .exclude(venuename__endswith=' Road') \
              # .exclude(venuename__endswith=' Street') \
              # .exclude(venuename__endswith=' Terrace') \
              # .exclude(venuename__endswith=' Lane') \
              # .exclude(venuename__endswith=' Drive') \

        ordering = request.GET.get('ordering', '-venue_count')
        # Query venues count per filtered venuename
        venues_count_by_venuename = Venue.objects \
            .filter(venuename__in=filtered_names) \
            .values('venuename') \
            .annotate(venue_count=Count('id')) \
            .order_by(ordering)

        # Paginate the results
        paginated_venues = paginator.paginate_queryset(venues_count_by_venuename, request)
        
        # Create a list of JSON objects with venuename and venue count
        name_and_venues = []
        for item in paginated_venues:
            venuename = item['venuename']
            venue_count = item['venue_count']
            name_venue = {'venuename': venuename, 'count': venue_count}
            name_and_venues.append(name_venue)

        return paginator.get_paginated_response(name_and_venues)
    