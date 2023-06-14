import requests
from bs4 import BeautifulSoup
import json

# with open('movie_pages.json') as data:
# 	movies = json.load(data)


movies = [
	"https://yts.mx/movies/the-longest-weekend-2022",
  	"https://yts.mx/movies/jaguar-lives-1979",
 	"https://yts.mx/movies/wild-daze-2020",
	"https://yts.mx/movies/hollywood-fringe-2020"
]

for movie in movies:
	headers = {
    	    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    	}
	res = requests.get(movie, headers=headers)
	document = BeautifulSoup(res.content, 'html.parser')
	title = document.select('#movie-info > div.hidden-xs > h1')[0].decode_contents() +' '+ document.select('#movie-info > div.hidden-xs > h2')[0].decode_contents() 
	image = document.select('#movie-poster > img')[0].get('src')
	teaser = document.select('#synopsis > p:nth-child(2)')[0].decode_contents()
	magnets = document.select('.magnet-download')
	torrents = document.select('.download-torrent.button-green-download2-big')

	tempDict = {
	"title": title,
	"teaser": teaser,
	"img": image,
	}
	print(tempDict)