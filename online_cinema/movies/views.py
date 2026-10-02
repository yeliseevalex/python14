from django.shortcuts import render, get_object_or_404
from django.utils.deprecation import django_file_prefixes

from .models import Movie, Genre

from interactions.models import Favorite, Rating
from django.db.models import Avg

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

    average_rating = movie.ratings.aggregate(average=Avg('value'))['average']
    rating_count = movie.ratings.count()
    user_rating = None

    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(
            user=request.user,
            movie_id=movie_id
        ).first()

    is_favorite = False

    if request.user.is_authenticated:
        is_favorite = movie.favorited_by.filter(
            user_id=request.user.id
        ).exists()

    comments = movie.comments.filter(
        parent__isnull=True
    ).select_related("user").prefetch_related("replies__user")

    return render(
        request,
        "movies/detail.html",
        {
            "movie": movie,
            "is_favorite": is_favorite,
            "average_rating": average_rating,
            "rating_count": rating_count,
            "user_rating": user_rating,
            "comments": comments
        }
    )