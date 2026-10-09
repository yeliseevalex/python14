from multiprocessing import context

from django.core import paginator
from django.shortcuts import render, get_object_or_404
from django.utils.deprecation import django_file_prefixes
from django.core.paginator import Paginator
from pip._internal.models import candidate

from .models import Movie, Genre
from .recommendations import get_recommendations, get_user_recommendations

from interactions.models import Favorite, Rating
from django.db.models import Avg
import random

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

def format_duration(minutes):
    hours, remaining_minutes = divmod(minutes, 60)

    if hours and remaining_minutes:
        return f"{hours} год {remaining_minutes} хв"

    if hours:
        return f"{hours} год"

    return f"{remaining_minutes} хв"


def time_picker(request):
    context = {
        "hours": 2,
        "minutes": 0,
        "movies": []
    }

    if request.method != "POST":
        return render(request, 'movies/time_picker.html', context)

    try:
        hours = int(request.POST.get("hours", 0))
        minutes = int(request.POST.get("minutes", 0))
    except (TypeError, ValueError):
        context["error"] = "Вкажіть коректний час."
        return render(request, 'movies/time_picker.html', context)

    if hours < 0 or hours > 24 or minutes not in (0, 15, 30, 45):
        context["error"] = "Перевірте введений час."
        return render(request, 'movies/time_picker.html', context)

    total_minutes = hours * 60 + minutes

    if total_minutes <= 0 or total_minutes > 1440:
        context["error"] = "Вкажіть час від 15 хвилин до 24 годин."
        return render(request, 'movies/time_picker.html', context)

    excluded_ids = []

    for movie_id in request.POST.getlist("excluded_ids"):
        try:
            excluded_ids.append(int(movie_id))
        except (TypeError, ValueError):
            continue

    base_movies = Movie.objects.filter(
        duration__gt=0,
        duration__lte=total_minutes
    ).select_related("genre")

    candidates = list(base_movies.exclude(id__in=excluded_ids))

    if not candidates:
        candidates = list(base_movies)

    if not candidates:
        context.update({
            "hours": hours,
            "minutes": minutes,
            "error": "На жаль, не знайшли фільмів для цього часу."
        })
        return render(request, 'movies/time_picker.html', context)

    best_movies = []
    best_duration = 0

    for _ in range(40):
        shuffled_movies = candidates.copy()
        random.shuffle(shuffled_movies)

        selected_movies = []
        used_minutes = 0

        for movie in shuffled_movies:
            if used_minutes + movie.duration <= total_minutes:
                selected_movies.append(movie)
                used_minutes += movie.duration

            if used_minutes > best_duration:
                best_movies = selected_movies
                best_duration = used_minutes

    for movie in best_movies:
        movie.duration_display = format_duration(movie.duration)

        print(movie.duration)
        print(format_duration(movie.duration))
        print(movie.duration_display)

    context.update({
        "hours": hours,
        "minutes": minutes,
        "movies": best_movies,
        "total_minutes": total_minutes,
        "used_minutes": best_duration,
        "remaining_minutes": total_minutes - best_duration,
        "availble_time_display": format_duration(total_minutes),
        "used_time_display": format_duration(best_duration),
        "remaining_time_display": format_duration(total_minutes - best_duration),
    })

    return render(request, 'movies/time_picker.html', context)








