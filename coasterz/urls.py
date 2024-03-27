from django.conf import settings
from django.conf.urls.static import static
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
  path('api/notes/', include('notes.urls')),
  path('api/events/', include('events.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)