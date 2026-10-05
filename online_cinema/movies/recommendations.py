from .models import Movie
from interactions.models import WatchHistory
from collections import Counter

def get_recommendations(movie, limit=5):
    movies = Movie.objects.exclude(id = movie.id)
    recommendations = []

    for candidate in movies:
        score = 0

        if candidate.genre == movie.genre:
            score += 5

        movie_actors = set(movie.actors.values_list("id", flat=True))
        candidate_actors = set(candidate.actors.values_list("id", flat=True))

        common_actors = (movie_actors & candidate_actors)

        score += len(common_actors) * 3

        if candidate.year and movie.year:
            if candidate.year == movie.year:
                score += 2
            elif abs(candidate.year - movie.year) <= 3:
                score += 1


        if score > 0:
            recommendations.append((candidate, score))

    recommendations.sort(key=lambda item: item[1], reverse=True)

    return recommendations[:limit]


def calculate_similarity(movie, candidate):
    score = 0
    if movie.genre.id == candidate.genre.id:
        score += 5

    movie_actors = {
        actor.id for actor in movie.actors.all()
    }

    candidate_actors = {
        actor.id for actor in candidate.actors.all()
    }

    common_actors = (movie_actors & candidate_actors)

    score += len(common_actors) * 3

    if candidate.year and movie.year:
        if candidate.year == movie.year:
            score += 2
        elif abs(candidate.year - movie.year) <= 3:
            score += 1

    return score

def get_user_recommendations(user, limit=5):
    history = WatchHistory.objects.filter(user=user).select_related('movie')

    if not history.exists():
        return []

    genre_counter = Counter(item.movie.genre.id for item in history if item.movie.genre.id)

    watched_movies_ids = [item.movie.id for item in history]

    movies = Movie.objects.exclude(id__in=watched_movies_ids).select_related("genre").prefetch_related('actors')

    recommendations = []

    for candidate in movies:
        score = 0
        score += genre_counter.get(candidate.genre.id, 0)

        for item in history:
            similarity = calculate_similarity(item.movie, candidate)

            score += similarity

        if score > 0:
            recommendations.append(
                {
                    "movie": candidate,
                    "score": score,
                 }
            )

    recommendations.sort(key=lambda item: item["score"], reverse=True)
    return recommendations[:limit]