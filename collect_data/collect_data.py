from bs4 import BeautifulSoup
import requests
# with open("example.html", "r") as f:
#     html = f.read()

# soup = BeautifulSoup(html, "html.parser")
# print(soup)
# divs = soup.find("div")
# for p in divs.find_all("p"):
#     print(p.get_text(strip=True))

# descriptions = soup.find_all("p", class_ = "description")
# print(descriptions)

# link = soup.find("div", {"class" : "movie"}).find_all("a")[-1].get("href")
# print(link)

# div_find = soup.find("body").find_all("div")[1]
# print(div_find)
#
# print("="*20)
#
# div_select = soup.select("body > div:nth-child(2)")
# print(div_select)

# print(list(div_select[0].children))

response = requests.get("https://www.rottentomatoes.com/browse/movies_in_theaters/sort:newest")
# with open(r"D:\practice14\collect_data\movies.html", "w", encoding="utf-8") as f:
#     f.write(response.text)
#
# with open(r"D:\practice14\collect_data\movies.html", "r", encoding="utf-8") as f:
#     soup = BeautifulSoup(f.read(), "html.parser")

soup = BeautifulSoup(response.text, "html.parser")
movies_in_page = soup.find("div", {"class": "discovery-tiles__wrap"})
all_movies_in_page = movies_in_page.find_all("div", {"class": "flex-container"})

movie_links = []
for movie_info in all_movies_in_page:
    movie_link = movie_info.find("a", {"class": "js-tile-link"})
    movie_link = "https://www.rottentomatoes.com" + movie_link.get("href")
    movie_links.append(movie_link)


movie_links = movie_links

result = {}

# result = {
#     "Movie1": {
#         "title" : "Runner"
#     }
# }
info = {}

for i, movie_url in enumerate(movie_links):

    res_movie = requests.get(movie_url)
    soup_movie = BeautifulSoup(res_movie.text, "html.parser")
    # with open("runner_2026.html", "w", encoding="utf-8") as f:
    #     f.write(res_movie.text)
    #
    # with open("runner_2026.html", "r", encoding="utf-8") as f:
    #     soup_movie = BeautifulSoup(f, "html.parser")

    hero_wrap = soup_movie.find("div", {"class": "media-hero-wrap"})
    title = hero_wrap.find("rt-text", {"slot": "title"}).get_text(strip=True)
    print(title)
    info["title"] = title

    main_wrap = soup_movie.find("div", {"id": "main-wrap"})

    media_scorecard = main_wrap.find("div", {"class": "media-scorecard"})
    img_link = media_scorecard.find("rt-img", {"slot": "poster-image"}).get("src")
    # print(img_link)
    info["img_link"] = img_link


    media_info = main_wrap.find("section", {"class": "media-info"})

    description_info = media_info.find("div", {"class": "synopsis-wrap"})
    try:
        description = description_info.find("rt-text", {"data-qa": "synopsis-value"}).get_text(strip=True)
    except Exception as error:
        print(f"Error: {error}")
        description = None
    # print(description)
    info["description"] = description

    dl = media_info.find("dl")
    category_wrap = dl.find_all("div", {"class": "category-wrap"})
    years = []
    duration = 0
    genre = None
    for item in category_wrap:
        dt_text = item.find("dt", {"class": "key"}).get_text(strip=True)
        if "Release Date" in dt_text or "Rerelease Date" in dt_text:
            dd = item.find("dd", {"data-qa": "item-value-group"})
            date = dd.find("rt-text", {"data-qa": "item-value"}).get_text(strip=True)
            year = date.split(',')[1].strip()
            years.append(int(year))
        if "Runtime" in dt_text:
            dd = item.find("dd", {"data-qa": "item-value-group"})
            duration = dd.find("rt-text", {"data-qa": "item-value"}).get_text(strip=True).split(" ")
            if "h" in duration[0]:
                duration = int(duration[0].replace("h", '')) * 60 + int(duration[1].replace("m", ''))
            else:
                duration = int(duration[0])
        if "Genre" in dt_text:
            dd = item.find("dd", {"data-qa": "item-value-group"})
            genre = dd.find("rt-link", {"data-qa": "item-value"}).get_text(strip=True)


    # print(duration)
    year = max(years)
    # print(year)
    years.clear()
    # print(genre)
    info["duration"] = duration
    info["genre"] = genre
    info["year"] = year

    cast_and_crew_url = movie_url + "/cast-and-crew"
    res_cast = requests.get(cast_and_crew_url)
    soup_cast = BeautifulSoup(res_cast.text, "html.parser")
    # with open("runner_2026.html", "w", encoding="utf-8") as f:
    #     f.write(res_cast.text)
    #
    # with open("runner_2026.html", "r", encoding="utf-8") as f:
    #     soup_cast = BeautifulSoup(f, "html.parser")

    content_wrap = soup_cast.find("section", {"class": "cast-and-crew"})
    cast_and_crew_card = content_wrap.find_all("cast-and-crew-card")

    actors_links = []
    for cast_and_crew in cast_and_crew_card:
       if "Actor" in cast_and_crew.text or "Self" in cast_and_crew.text:
           actor_link = "https://www.rottentomatoes.com/" + cast_and_crew.get("media-url")
           actors_links.append(actor_link)

    actors = []
    for actor_url in actors_links:
        res_actor = requests.get(actor_url)
        soup_actor = BeautifulSoup(res_actor.text, "html.parser")
        # with open("runner_2026.html", "w", encoding="utf-8") as f:
        #     f.write(res_actor.text)
        #
        # with open("runner_2026.html", "r", encoding="utf-8") as f:
        #     soup_actor = BeautifulSoup(f, "html.parser")

        name = soup_actor.find("h1", {"class": "celebrity-bio__h1"}).get_text(strip=True)
        print(name)
        year_actor = None
        div_celebrity_info = soup_actor.find("div", {"class": {"celebrity-bio__info"}})
        p_info = div_celebrity_info.find_all("p", {"class": "celebrity-bio__item"})
        for p in p_info:
            if "Birthday" in p.find("rt-text").text:
                year_actor = p.get_text(strip=True).split(",")[-1].strip()

        if "Not Available" in year_actor:
            year_actor = None

        year_actor = int(year_actor) if year_actor else None
        # print(year_actor)
        actors.append((name, year_actor))

    info["actors"] = actors

    result[f"movie{i+1}"] = info
    print("*" * 50)
    print(info)
    info = {}

print("=" * 100)
print(result)
import json

with open("result.json", "w") as f:
    json.dump(result, f, indent=4)