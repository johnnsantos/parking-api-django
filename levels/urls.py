from django.urls import path
from .views import ListCreateLevels

urlpatterns = [path("levels/", ListCreateLevels.as_view())]
