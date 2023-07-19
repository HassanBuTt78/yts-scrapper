import requests
from bs4 import BeautifulSoup
import json


def scrape_movie_links(base_url, total_pages):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    all_links = []
    for page in range(1, total_pages + 1):
        url = f"{base_url}?page={page}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            links = soup.select("div.browse-movie-wrap > a")            
            all_links.extend(link["href"] for link in links)
            print(f"Page {page} scraped.")
        else:
            print(
                f"Failed to fetch page {page}. Status code: {response.status_code}")
    return all_links


if __name__ == "__main__":
    base_url = "https://yts.mx/browse-movies"
    total_pages = 2610

    movie_links = scrape_movie_links(base_url, total_pages)

    # Storing the scraped links in a JSON file
    with open("lists/movie_links.json", "w") as file:
        json.dump(movie_links, file)

    print("Scraping complete. Links stored in 'movie_links.json'.")

