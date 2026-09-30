from django.contrib import admin

from .models import Favorite, WatchHistory, Rating

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "movie",
        "created_at"
    ]

    list_filter = [
        "created_at"
    ]

    search_fields = [
        "user__username",
        "movie__title"
    ]

@admin.register(WatchHistory)
class WatchHistoryAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'movie',
        'watched_at',
        'watch_duration'
    ]

    list_filter = [
        'watched_at'
    ]

    search_fields = [
        'user__username',
        'movie__title'
    ]

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'movie',
        'value',
        'created_at',
        'updated_at'
    ]

    list_filter = [
        'value',
        'created_at'
    ]

    search_fields = [
        "user__username",
        'movie__title'
    ]