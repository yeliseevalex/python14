from django.contrib import admin

from .models import Actor, Genre, Movie
from django.utils.html import format_html

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "movie_count"
    )

    search_fields = (
        "name",
    )

    def movie_count(self, obj):
        return obj.genre_movies.count()

    movie_count.short_description = "Movies"


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "birth_year",
        "movie_count"
    )

    search_fields = (
        "name",
    )

    list_filter = (
        "birth_year",
    )

    def movie_count(self, obj):
        return obj.actors_movies.count()

    movie_count.short_description = "Movies"


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        "poster_preview",
        "id",
        "title",
        "year",
        "genre",
        "duration",
        "actor_count"
    )

    search_fields = (
        "title",
        "description",
        "actors__name"
    )

    list_filter = (
        "genre",
        "year",
    )

    ordering = (
        "-year",
        "title"
    )

    def actor_count(self, obj):
        return obj.actors.count()

    actor_count.short_description = "Actors"

    def poster_preview(self, obj):
        if not obj.img_link:
            return "No image"

        return format_html(
            '<img src="{}" width="60" height="90 '
            'style="object-fit: cover; border-radius: 20px;"/>',
            obj.img_link
        )

    poster_preview.short_description = "Preview"






