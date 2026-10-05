from django.core import paginator
from django.shortcuts import render, get_object_or_404
from django.utils.deprecation import django_file_prefixes
from django.core.paginator import Paginator

from .models import Movie, Genre
from .recommendations import get_recommendations, get_user_recommendations

from interactions.models import Favorite, Rating
from django.db.models import Avg

def home(request):
    movies = Movie.objects.all()
    genres = Genre.objects.all()

    search = request.GET.get("search", "")
    select_genre = request.GET.get("genre", "")
    select_sort = request.GET.get("sort", "")
    query_params = request.GET.copy()
    query_params.pop("page", None)

    if search:
        movies = movies.filter(
            title__icontains=search
        )

    if select_genre:
        movies = movies.filter(
            genre__name=select_genre
        )

    if select_sort == "newest":
        movies = movies.order_by("-year")

    elif select_sort == "oldest":
        movies = movies.order_by("year")

    elif select_sort == "shortest":
        movies = movies.order_by("duration")

    elif select_sort == "longest":
        movies = movies.order_by("-duration")
    else:
        movies = movies.order_by("-id")

    recommendations = []
    if request.user.is_authenticated:
        recommendations = get_user_recommendations(request.user)

    paginator = Paginator(movies, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "movies/home.html",
        {
            "movies": movies,
            "recommendations": recommendations,
            "page_obj": page_obj,
            "genres": genres,
            "search": search,
            "selected_genre": select_genre,
            "selected_sort": select_sort,
            "query_params": query_params
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

    recommendations = get_recommendations(movie)

    return render(
        request,
        "movies/detail.html",
        {
            "movie": movie,
            "recommendations": recommendations,
            "is_favorite": is_favorite,
            "average_rating": average_rating,
            "rating_count": rating_count,
            "user_rating": user_rating,
            "comments": comments
        }
    )