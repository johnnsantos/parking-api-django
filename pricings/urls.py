from django.urls import path
from .views import ListCreatePricing

urlpatterns = [path("pricings/", ListCreatePricing.as_view())]
