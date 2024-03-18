from django.db import models
# Create your models here.
class Venue(models.Model):
  fsa_id = models.BigIntegerField()
  venuename = models.CharField(max_length=255)
  slug = models.CharField(max_length=255)
  venuetype = models.CharField(max_length=255)
  address = models.CharField(max_length=255)
  address2 = models.CharField(max_length=255)
  town = models.CharField(max_length=255)
  county = models.CharField(max_length=255)
  postcode = models.CharField(max_length=255)
  postalsearch = models.CharField(max_length=255)
  telephone = models.CharField(max_length=255)
  easting = models.CharField(max_length=255)
  northing = models.CharField(max_length=255)
  latitude = models.CharField(max_length=255)
  longitude = models.CharField(max_length=255)
  local_authority = models.CharField(max_length=255)
  website = models.CharField(max_length=255)
  photo = models.ImageField(upload_to='media/venues')
  is_live = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  def __str__(self):
    return f"{self.venuename}, {self.address}, {self.town}, {self.county}"