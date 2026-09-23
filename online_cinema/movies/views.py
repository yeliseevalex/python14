from unittest import runner

from django.shortcuts import render, get_object_or_404

from .models import Movie, Genre

def home(request):
    movies = Movie.objects.all()
    genres = Genre.objects.all()

    search = request.GET.get("search")
    genre = request.GET.get("genre")
    sort = request.GET.get("sort")

    if search:
        movies = movies.filter(
            title__icontains=search
        )

    if genre:
        movies = movies.filter(
            genre__name=genre
        )

    if sort == "newest":
        movies = movies.order_by("-year")

    elif sort == "oldest":
        movies = movies.order_by("year")

    elif sort == "shortest":
        movies = movies.order_by("duration")

    elif sort == "longest":
        movies = movies.order_by("-duration")

    return render(
        request,
        "movies/home.html",
        {
            "movies": movies,
            "genres": genres,
            "search": search or "",
            "selected_genre": genre or "",
            "selected_sort": sort or ""
        }
    )

def movie_detail(request, movie_id):
    movie = get_object_or_404(
        Movie,
        id=movie_id
    )

    return render(
        request,
        "movies/detail.html",
        {
            "movie": movie
        }
    )