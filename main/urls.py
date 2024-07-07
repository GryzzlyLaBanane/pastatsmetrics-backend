from django.urls import path, include
from . import views

app_name = "pastats"


urlpatterns = [
    path("", views.pastats, name="pastats"),
]
