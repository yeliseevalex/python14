from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from movies.models import Movie
from .models import Favorite, WatchHistory, Rating


@login_required
def toggle_favorite(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    favorite = Favorite.objects.filter(
        user=request.user,
        movie=movie
    ).first()

    if favorite:
        favorite.delete()

    else:
        Favorite.objects.create(
            user=request.user,
            movie=movie
        )

    return redirect(
        'movie_detail',
        movie_id=movie_id
    )

@login_required
def watch_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    watch_seconds = max(1, round(movie.duration / 10))

    return JsonResponse(
        {
            "movie_id": movie_id,
            "title": movie.title,
            "duration": movie.duration,
            "watch_second": watch_seconds
        }
    )

@login_required
@require_POST
def complete_watch(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    watch_seconds = max(1, round(movie.duration / 10))

    WatchHistory.objects.create(
        user=request.user,
        movie=movie,
        watch_duration=watch_seconds
    )

    return JsonResponse(
        {
            "success": True,
            "message": "Перегляд завершено!"
        }
    )

@login_required
@require_POST
def rate_movie(request, movie_id):
    movie = get_object_or_404(
        Movie,
        id=movie_id
    )

    value = int(request.POST.get("rating", 0))

    if value < 1 or value > 5:
        return JsonResponse(
            {
                "success": False,
                "error": "Оцінка повинна бути від 1 до 5."
            },
            status=400
        )

    rating, created = Rating.objects.update_or_create(
        user=request.user,
        movie=movie,
        defaults={
            "value":value
        }
    )

    return JsonResponse(
        {
            "success": True,
            "value": rating.value,
            "created": created
        }
    )
