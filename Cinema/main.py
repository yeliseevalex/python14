from database import SessionLocal, engine
from models import Base, User
from seed import seed_database

import services
import queries


Base.metadata.create_all(bind=engine)

def print_separator():
    print("═"*50)

def print_movies(movies):
    for movie in movies:
        print_separator()
        print(f"Title: {movie.title}")
        print(f"Description: {movie.description}")
        print(f"Year: {movie.year}")

    print_separator()

def print_genres(genres):
    for genre in genres:
        print_separator()
        print(f"Name: {genre.name}")

    print_separator()

def print_movie_details(movie_details):
    print_separator()
    for key, value in movie_details.items():
        if isinstance(value, list):
            print(f"{key.title()}: ")
            for item in value:
                print(f"\t-{item.name}")
        else:
            print(f"{key.title()}: {value}")
    print_separator()

def print_user_details(movie_details):
    print_separator()
    for key, value in movie_details.items():
        if isinstance(value, list):
            print(f"{key.title()}: ")
            for item in value:
                print(f"\t-{item}")
        else:
            print(f"{key.title()}: {value}")
    print_separator()

def main():
    # seed_database()
    with SessionLocal() as session:
        while True:
            print("""
╔══════════════════════════════════════╗
║             ONLINE CINEMA            ║
╠══════════════════════════════════════╣
║                                      ║
║  1. Переглянути фільми               ║
║  2. Знайти фільм                     ║
║  3. Переглянути інформацію про фільм ║
║  4. Переглянути жанри                ║
║  5. Додати фільм до обраного         ║
║  6. Оцінити фільм                    ║
║  7. Переглянути фільм                ║
║  8. Історія переглядів               ║
║  9. Моя статистика                   ║
║ 10. Рекомендації                     ║
║                                      ║
║ ───────── АДМІН ──────────────────── ║
║ 11. Додати фільм                     ║
║ 12. Редагувати фільм                 ║
║ 13. Видалити фільм                   ║
║ 14. Статистика фільмів               ║
║                                      ║
║  0. Вийти                            ║
╚══════════════════════════════════════╝
            """)

            choice = input("Ваш вібір: ")

            if choice == "1":
                movies = services.get_all_movies(session)
                print_movies(movies)

            elif choice == "2":
                query = input("Введіть назву або частину назви: ")
                movies = queries.search_movie(session, query)
                print_movies(movies)

            elif choice == "3":
                movie_id = input("Введіть movie_id: ")
                movie = queries.get_movie_details(session, movie_id)
                print_movie_details(movie)

            elif choice == "4":
                genres = services.get_all_genres(session)
                print_genres(genres)

            elif choice == "5":
                user_id = int(input("Введіть user_id: "))
                movie_id = input("Введіть movie_id: ")

                result = services.add_to_favorites(session, movie_id, user_id)

                if result:
                    print("Фільм додано до обраного")
                else:
                    print("Не вдалося додати фільм")

            elif choice == "6":
                user_id = int(input("Введіть user_id: "))
                movie_id = input("Введіть movie_id: ")
                value =  int(input("Оцінка 1-10: "))

                try:
                    services.rate_movie(session, movie_id, user_id, value)
                    print("Оцінку успішно додано")

                except ValueError as error:
                    print(f"Помилка: {error}")

            elif choice == "7":
                user_id = int(input("Введіть user_id: "))
                movie_id = input("Введіть movie_id: ")
                try:
                    result = services.watch_movie(session, movie_id, user_id)
                    if result:
                        print("Приємного перегляду")
                    else:
                        print("Немає активноі підписки")
                except ValueError as error:
                    print(f"Помилка: {error}")

            elif choice == "8":
                user_id = int(input("Введіть user_id: "))
                movies = queries.get_user_history(session, user_id)
                print_separator()
                for movie in movies:
                    print(f"Title: {movie}")
                print_separator()

            elif choice == "9":
                user_id = int(input("Введіть user_id: "))
                statistics = queries.get_user_statistics(session, user_id)
                print_user_details(statistics)

            elif choice == "10":
                user_id = int(input("Введіть user_id: "))
                recommended = queries.recommend_movies(session, user_id)
                print_separator()
                for movie in recommended:
                    print(f"Title: {movie}")
                print_separator()








if __name__ == "__main__":
    main()