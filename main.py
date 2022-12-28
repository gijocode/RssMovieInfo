import concurrent.futures
import json
import re
from urllib.parse import quote

import feedparser
import requests
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader  # pip install Jinja2


def get_movie_name_from_rss_string(rssStr):
    return re.split("\([1-3][0-9]{3}\)", rssStr)[0].strip()


def get_movie_details_from_rss(rssUrl):
    rssData = feedparser.parse(rssUrl)
    movies_names = {
        get_movie_name_from_rss_string(movie.get("title"))
        for movie in rssData.get("entries")
    }
    return movies_names


def make_async_func(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def get_movie_info(movie_title):
    url = f"https://www.imdb.com/find?q={quote(movie_title)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    movie_div = soup.find("li", class_="find-title-result")
    if movie_div:
        movie_url = f"https://www.imdb.com/{movie_div.find('a', class_='ipc-metadata-list-summary-item__t')['href']}"
        movie_response = requests.get(movie_url, headers=headers)
        movie_soup = BeautifulSoup(movie_response.text, "html.parser")
        synopsis = movie_soup.find("span", attrs={"data-testid": "plot-l"}).text.strip()
        cast = ",".join(
            [
                movie_actor.text
                for movie_actor in movie_soup.find_all(
                    "a", attrs={"data-testid": "title-cast-item__actor"}, limit=5
                )
            ]
        )
        movie = {"title": movie_title, "synopsis": synopsis, "cast": cast}
        return movie
    else:
        return None


def get_rss_movie_info(rssName, rssUrl):
    movies = get_movie_details_from_rss(rssUrl)
    rssFeedMovieInfo = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        movie_infos = [
            executor.submit(make_async_func(get_movie_info), movie) for movie in movies
        ]
        for movie_info in concurrent.futures.as_completed(movie_infos):
            rssFeedMovieInfo.append(movie_info.result())
    return {rssName: rssFeedMovieInfo}


if __name__ == "__main__":
    env = Environment(loader=FileSystemLoader("templates/"))
    template = env.get_template("TableTemplate.html")  # the template file name

    allMovieInfo = {}
    with open("input/rssFeeds.json") as rssFile:
        rssDict = json.load(rssFile)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        rss_movie_infos = [
            executor.submit(make_async_func(get_rss_movie_info), rssName, rssUrl)
            for rssName, rssUrl in rssDict.items()
        ]
        for movie_info in concurrent.futures.as_completed(rss_movie_infos):
            allMovieInfo.update(movie_info.result())

    with open("movies_data.json", "w") as mdj:
        json.dump(allMovieInfo, mdj, indent=4)

    html = template.render(allMovieInfo=allMovieInfo)
    with open("renderedHtml.html", "w") as renderedHtml:
        renderedHtml.write(html)