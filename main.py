from bs4 import BeautifulSoup
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
import requests
import time
import json


try:

        uri = "mongodb+srv://Hassan:hassan@cluster0.wmrmexl.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(uri, server_api=ServerApi('1'))
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

        db = client.yts
        collection = db.movies


        #checking previous scrapped and dettermine next to scrape
        count_id = ObjectId('648cca91458f4a9821e72daa')
        count = collection.find_one({'_id': count_id})['count']
        count = int(count)
        print(f'*{count}* Pages has been Already Scrapped')
        with open('movie_pages.json') as data:
                movies = json.load(data)

        movies = movies[count:]

        print(f'*{len(movies)}* Pages to go')


        # magnet links formator
        def magnetExtract(magnets):
            magnetLinks = {}
            for magnet in magnets:
                magnetLink = {
                    last_two_words(magnet.get('title')): magnet.get('href')
                }
                magnetLinks.update(magnetLink)
            return magnetLinks


        def torrentExtract(torrents):
            torrentLinks = {}
            for torrent in torrents:
                torrentLink = {
                    last_two_words(torrent.get('title')): torrent.get('href')
                }
                torrentLinks.update(torrentLink)
            return torrentLinks


        def last_two_words(string):
            words = string.split()  # Split the string into words
            if len(words) >= 2:
                last_two_words = words[-2:]  # Extract the last two words
                return " ".join(last_two_words)  # Join the words back into a string
            else:
                return string  # Return the original string if it has less than two words


        def genreToArray(string):
            processedString = string.replace('/ ', '')
            genreArray = processedString.split()
            return genreArray


        for movie in movies:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
            }
            res = requests.get(movie, headers=headers)

            if res.status_code == 200:

                try:

                    document = BeautifulSoup(res.content, 'html.parser')
                    title = document.select('#movie-info > div.hidden-xs > h1')[0].decode_contents(
                    ) + ' ' + document.select('#movie-info > div.hidden-xs > h2')[0].text.strip()
                    image = document.select('#movie-poster > img')[0].get('src')
                    teaser = document.select(
                        '#synopsis > p:nth-child(2)')[0].decode_contents()
                    IMDB_rating = document.find(
                        'span', attrs={"itemprop": "ratingValue"}).decode_contents()
                    genre = document.select(
                        '#movie-info > div.hidden-xs > h2:nth-child(3)')[0].decode_contents()
                    magnets = document.select('.magnet-download')
                    torrents = document.select(
                        '.download-torrent.button-green-download2-big')

                    insert = {
                        "title": title,
                        "teaser": teaser,
                        "img": image,
                        "genre": genreToArray(genre),
                        "IMDB_rating": IMDB_rating,
                        "links": {
                            "magnets": magnetExtract(magnets),
                            "torrents": magnetExtract(torrents)
                        },
                        "devL": movie
                    }

                    collection.insert_one(insert)

                    count = count + 1
                    update = {'$set': {'count': count}}
                    collection.update_one({'_id': count_id}, update)
                    print(f'Scrapped "{title}" --- COUNT = {count}')

                except Exception as error:
                    print(f'an Exception Happened ************ ::: {str(error)}')
            else:
                print(f'failed to retrieve webpage status_code:{res.status_code}')

        client.close()
except Exception as error:
        print(f'There has been en error {error}')
        print('******************************************RESTARTING*************************************************')
        time.sleep(5)
