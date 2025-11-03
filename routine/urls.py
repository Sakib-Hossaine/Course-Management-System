from django.urls import path
from .views import routine



urlpatterns = [
   path("routine/", routine, name="routine"),
]