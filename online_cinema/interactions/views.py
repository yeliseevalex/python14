from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from movies.models import Movie
from .models import Favorite

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

