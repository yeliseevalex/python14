from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("movie/<int:movie_id>/", views.movie_detail, name="movie_detail"),
    path("time-picker/", views.time_picker, name="time_picker"),
]