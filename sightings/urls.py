from django.urls import path
from . import views

urlpatterns = [
  path('',views.sightings,name='sightings'),
]
