from django.contrib import admin
from django.urls import path, re_path, include
from . import views

urlpatterns = [
  path('admin/', admin.site.urls),
  re_path('login', views.login),
  re_path('signup', views.signup),
  re_path('get_user', views.get_user),
  re_path('favoured-venues/',views.FavouredVenuesAPIView),
  re_path('logout', views.logout),
  path('api/venues/', include('venues.urls')),
  path('api/notes/', include('notes.urls'))
]
