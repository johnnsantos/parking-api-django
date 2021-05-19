from django.urls import path
from .views import VehicleView

urlpatterns = [
    path("vehicles/", VehicleView.as_view()),
]
