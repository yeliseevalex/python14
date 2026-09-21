import json

from django.core.management import CommandParser
from django.core.management.base import BaseCommand

from movies.models import Movie, Genre, Actor

class Command(BaseCommand):
    help = "Import movies from JSON file"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "file_path",
            type=str
        )

    def handle(self, *args, **options):
        file_path = options["file_path"]

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        movies_created = 0
        actors_created = 0
        genres_created = 0

        for movie_data in data.values():
            genre, genre_created = Genre.objects.get_or_create(
                name=movie_data['genre']
            )

            if genre_created:
                genres_created += 1

            movie, movie_created = Movie.objects.get_or_create(
                title=movie_data['title'],
                img_link=movie_data['img_link'],
                description=movie_data['description'],
                duration=movie_data['duration'],
                year=movie_data['year'],
                genre=genre
            )

            if movie_created:
                movies_created += 1

            for actor_name, birth_year in movie_data['actors']:
               actor, actor_created = Actor.objects.get_or_create(
                    name=actor_name,
                    defaults={
                        "birth_year":birth_year,
                    }
               )

               if actor_created:
                   actors_created += 1

               movie.actors.add(actor)

        self.stdout.write(
            self.style.SUCCESS(
                f"Movies created: {movies_created} \n Actors created: {actors_created} \n Genres: {genres_created}"
            )
        )