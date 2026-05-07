from django.urls import path
from . import views

app_name = "travel_ai"

urlpatterns = [

    path("", views.index, name="index"),

    path("about/", views.about, name="about"),

    path("api/health/", views.api_health, name="api_health"),

    path("api/predict/", views.api_predict, name="api_predict"),

    path("api/destinations/", views.api_destinations, name="api_destinations"),

]