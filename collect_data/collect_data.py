import json
import logging
from bs4 import BeautifulSoup
import asyncio
import aiohttp
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


BASE_URL = "https://www.rottentomatoes.com"
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

async def fetch_html(session: aiohttp.ClientSession, url: str) -> str | None:
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.text()
    except Exception as error:
        print(f"Error {url}: {error}")
        return None

async def parse_page_links(session: aiohttp.ClientSession, page_num: int) -> list[str]:
    url = f"{BASE_URL}/browse/movies_in_theaters/sort:newest?page={page_num}"
    logging.info(f"Parsing page {url}")
    html = await fetch_html(session, url)
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")
    movies_in_page = soup.find("div", {"class": "discovery-tiles__wrap"})
    if not movies_in_page:
        return []

    movie_links = []
    for movie_info in movies_in_page.find_all("div", {"class": "flex-container"}):
        link_tag = movie_info.find("a", {"class": "js-tile-link"})
        if link_tag and link_tag.get("href"):
            movie_links.append(f"{BASE_URL}{link_tag.get("href")}")
    return movie_links

async def get_all_movies_links(session: aiohttp.ClientSession, max_page: int = 5) -> list[str]:
    tasks = [parse_page_links(session, page) for page in range(1, max_page + 1)]
    results = await asyncio.gather(*tasks)

    all_links = [link for sublist in results for link in sublist]
    return all_links

async def parse_actor_info(session: aiohttp.ClientSession, actor_url: str, semaphore: asyncio.Semaphore) -> tuple[str, int | None] | None:
    async with semaphore:
        html = await fetch_html(session, actor_url)
        if not html:
            return None

        soup = BeautifulSoup(html, "html.parser")
        h1_tag = soup.find("h1", {"class": "celebrity-bio__h1"})
        if not h1_tag:
            return None

        name = h1_tag.get_text(strip=True)
        year_actor = None

        div_celebrity_info = soup.find("div", {"class": {"celebrity-bio__info"}})
        if div_celebrity_info:
            for p in div_celebrity_info.find_all("p", {"class": "celebrity-bio__item"}):
                rt_text = p.find("rt-text")
                if rt_text and "Birthday" in rt_text.text:
                    birth_text = p.get_text(strip=True).split(",")[-1].strip()
                    if "Not Available" not in birth_text and birth_text.isdigit():
                        year_actor = int(birth_text)
                    break

        return name, year_actor

async def parse_cast_and_crew(session: aiohttp.ClientSession, movie_url: str, semaphore: asyncio.Semaphore) -> list[tuple[str, int | None]]:
    cast_url = f"{movie_url}/cast-and-crew"
    async with semaphore:
        html = await fetch_html(session, cast_url)

    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")
    content_wrap = soup.find("section", {"class": "cast-and-crew"})
    if not content_wrap:
        return []

    actor_tasks = []
    for card in content_wrap.find_all("cast-and-crew-card"):
        if "Actor" in card.text or "Self" in card.text:
            media_link = card.get("media-url")
            if media_link:
                actor_link = f"{BASE_URL}/{media_link.lstrip('/')}"
                actor_tasks.append(parse_actor_info(session, actor_link, semaphore))

    actors = await asyncio.gather(*actor_tasks)
    return [a for a in actors if a is not None]

async def parse_movie_details(session: aiohttp.ClientSession, movie_url: str, semaphore: asyncio.Semaphore) -> dict | None:
    async with semaphore:
        html = await fetch_html(session, movie_url)

    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")
    info = {}

    logging.info(f"Parsing movie details for {movie_url}")

    hero_wrap = soup.find("div", {"class": "media-hero-wrap"})
    info["title"] = (
        hero_wrap.find("rt-text", {"slot": "title"}).get_text(strip=True)
        if hero_wrap and hero_wrap.find("rt-text", {"slot": "title"})
        else "N/A"
    )

    main_wrap = soup.find("div", {"id": "main-wrap"})
    if not main_wrap:
        return None

    media_scorecard = main_wrap.find("div", {"class": "media-scorecard"})
    info["img_link"] = (
        media_scorecard.find("rt-img", {"slot": "poster-image"}).get("src")
        if media_scorecard and media_scorecard.find("rt-img", {"slot": "poster-image"})
        else None
    )

    media_info = main_wrap.find("section", {"class": "media-info"})
    if media_info:
        description_info = media_info.find("div", {"class": "synopsis-wrap"})
        info["description"] = (
            description_info.find("rt-text", {"data-qa": "synopsis-value"}).get_text(strip=True)
            if description_info and description_info.find("rt-text", {"data-qa": "synopsis-value"})
            else None
        )

        years, duration, genre = [], 0, None
        dl = media_info.find("dl")
        if dl:
            for item in dl.find_all("div", {"class": "category-wrap"}):
                dt = item.find("dt", {"class": "key"})
                dd = item.find("dd", {"data-qa": "item-value-group"})
                if not dt or not dd:
                    continue

                dt_text = dt.get_text(strip=True)
                if "Release Date" in dt_text or "Rerelease Date" in dt_text:
                    date_tag = dd.find("rt-text", {"data-qa": "item-value"})
                    if date_tag:
                        parts = date_tag.get_text(strip=True).split(",")
                        if len(parts) > 1 and parts[1].strip().isdigit():
                            years.append(int(parts[1].strip()))

                elif "Runtime" in dt_text:
                    runtime_tag = dd.find("rt-text", {"data-qa": "item-value"})
                    if runtime_tag:
                        dur_parts = runtime_tag.get_text(strip=True).split(" ")
                        if len(dur_parts) >= 2 and "h" in dur_parts[0] and "m" in dur_parts[1]:
                            hours = int(dur_parts[0].replace("h", ''))
                            minutes = int(dur_parts[1].replace("m", ''))
                            duration = hours * 60 + minutes
                        elif len(dur_parts) >= 1 and dur_parts[0].isdigit():
                            duration = int(dur_parts[0])

                elif "Genre" in dt_text:
                    genre_tag = dd.find("rt-link", {"data-qa": "item-value"})
                    if genre_tag:
                        genre = genre_tag.get_text(strip=True)

        info["duration"] = duration
        info["genre"] = genre
        info["year"] = max(years) if years else None

    info["actors"] = await parse_cast_and_crew(session, movie_url, semaphore)
    return info

async def main():
    semaphore = asyncio.Semaphore(15)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Mobile Safari/537.36'
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        logging.info("Collecting movies...")
        movie_links = await get_all_movies_links(session, max_page=5)
        logging.info(f"{len(movie_links)} movies collected")

        logging.info("Parsing movies data...")
        tasks = [parse_movie_details(session, url, semaphore) for url in movie_links]
        parsed_movies = await asyncio.gather(*tasks)

        result = {}
        for i, movie_data in enumerate(parsed_movies):
            if movie_data:
                result[f"movie{i+1}"] = movie_data

    with open("movies.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)
    logging.info("Done! movies.json has been saved")

if __name__ == "__main__":
    asyncio.run(main())
