from bs4 import BeautifulSoup
from Movie import Movie
from datetime import datetime

import re
import sys
import Common
import Movie

HOME_URL = 'https://filmforum.org/'
DIRECTOR_KEY_WORD = 'directed by'
DIRECTOR_DELIMINATORS = ',|and'
MOVIE_URL_PREFIX = 'https://filmforum.org/film/'
FILM_FORUM_NAME = 'Film Forum'

# input: the soup created by the 'urgent' container on the movie page
def parseDirectors(soup):
    directors = []
    for info in soup.findChildren(recursive=False):
        if DIRECTOR_KEY_WORD in info.text.lower():
            for director in re.split(DIRECTOR_DELIMINATORS, info.text.lower().split(DIRECTOR_KEY_WORD)[1]):
                directors.append(director.encode('utf-8').strip())

    return directors

def parseMovieFromPage(soup, movie):
    title = soup.find('h1', {'class': 'main-title'}).text
    production_info = soup.find('div', {'class': 'urgent'})
    directors = parseDirectors(production_info)

    movie.title = title
    movie.directors = directors

def createMovie(showdate, movie_schedule):
    movie = Movie.Movie()

    movie.showdate = showdate
    movie.theater = FILM_FORUM_NAME

    # process movie url
    for link in movie_schedule.find_all('a'):
        href = link['href']
        if (href.startswith(MOVIE_URL_PREFIX)):
            movie.show_url = href

    if movie.show_url == None:
        print 'Cannot parse the movie page url on Film Forum!'
        return None

    parseMovieFromPage(Common.getPageSoup(movie.show_url), movie)

    for showtime in movie_schedule.find_all('span'):
        movie.addShowTime(movie.showdate, showtime.text)

    return movie

def getMoviesByDate(input_date):
    date = datetime.strptime(input_date, Movie.DATE_FORMAT)
    today = date.today()
    offset = date.day - today.day

    movies = []

    if date.year != today.year or date.month != today.month or offset > 6:
        raise ValueError('Cannot get movies for the day: {0}. Today is {1}'.format(date, today))
    else:
        soup = Common.getPageSoup(HOME_URL)
        for schedule in soup.find('div', {'id': 'tabs-{0}'.format(offset)}).findChildren(recursive=False):
            movie = createMovie(input_date, schedule)
            if movie is None:
                continue
            movies.append(movie)
        print 'Found {0} movies from {1} on {2}'.format(len(movies), FILM_FORUM_NAME, input_date)
        return movies


def main():
    reload(sys)
    sys.setdefaultencoding('utf8')

    date = '2018-01-14'
    movies = getMoviesByDate(date)
    print movies


if __name__ == '__main__':
    main()