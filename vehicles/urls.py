from django.urls import path
from .views import VehicleView

urlpatterns = [
    path("vehicles/", VehicleView.as_view()),
    path("vehicles/<int:vehicle_id>/", VehicleView.as_view()),
]
