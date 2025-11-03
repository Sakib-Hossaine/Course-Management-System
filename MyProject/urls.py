from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
   
    path("signup/", views.signup, name="signup"),
    # Other app urls
    path("", include("users.urls")),
    path("", include("courses.urls")),
    path("", include("notes.urls")),
    path("", include('routine.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
