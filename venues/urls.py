from django.urls import path
from .views import VenueListView, VenueAdd, VenueDetail, VenueFSA, VenueCounties, VenueTowns

urlpatterns = [
    path('all/', VenueListView.as_view(), name='venue-list'),
    path('add/', VenueAdd.as_view(), name='venue-add'),
    path('fsa/<int:fsa_id>/', VenueFSA.as_view(), name='venue-fsa'),
    path('<int:id>', VenueDetail.as_view(), name='venue-detail'),
    path('counties/', VenueCounties.as_view(), name='venue-county'),
    path('towns/', VenueTowns.as_view(), name='venue-towns'),
]