import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OMDB_API_KEY")

print("OMDB API KEY =", API_KEY)

BASE_URL = "http://www.omdbapi.com/"


def search_movies(title: str):
    url = f"{BASE_URL}?apikey={API_KEY}&s={title}"
    response = requests.get(url)
    return response.json()


def get_movie(imdb_id: str):
    url = f"{BASE_URL}?apikey={API_KEY}&i={imdb_id}"

    response = requests.get(url)

    data = response.json()

    print("MOVIE DETAILS =", data)

    return data