from bs4 import BeautifulSoup
from Movie import Movie
from datetime import datetime
from Series import PickleManager

import re
import sys
import Common
import Movie
import copy


HOME_URL = 'https://filmforum.org/'
DIRECTOR_KEY_WORD = 'directed by'
DIRECTOR_DELIMINATORS = ',|and'
MOVIE_URL_PREFIX = 'https://filmforum.org/film/'
FILM_FORUM_NAME = 'Film Forum'
SERIES_PAGE_DATE_FORMAT = '%A, %B %d'

# input: the soup created by the 'urgent' container on the movie page
def parseDirectors(soup):
    if soup is None:
        print 'looks like we cannot find the directors for this movie...'
        return

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

    soup = Common.getPageSoup(movie.show_url)
    if soup == None:
        return None

    parseMovieFromPage(Common.getPageSoup(movie.show_url), movie)

    for showtime in movie_schedule.find_all('span'):
        movie.addShowTime(movie.showdate, showtime.text)

    return movie

def getMoviesBySeries(series_name, series_url):
    movies = PickleManager.loadFromPickle(series_name)
    if movies is not None:
        return movies

    movies = []
    soup = Common.getPageSoup(series_url)

    if soup is None:
        print 'Cannot find the page: {0}'.format(series_url)

    films = soup.find_all('div', {'class': 'film-details'})

    if films is not None:
        for film in films:
            # intialize movie object
            movie = Movie.Movie()
            movie.theater = FILM_FORUM_NAME
            # title and show link
            title_div = film.find('h1', {'class': 'title'})
            if title_div is not None and title_div.a is not None:
                movie.title = title_div.a.text
                movie.show_url = title_div.a['href']
                # director
                # film_page_soup = Common.getPageSoup(movie.show_url)
                # if film_page_soup is not None and film_page_soup.find('div', {'class': 'urgent'}) is not None:
                #     movie.directors = parseDirectors(film_page_soup.find('div', {'class': 'urgent'}))
            # showtimes
            details_div = film.find('div', {'class': 'details'})
            if details_div is not None:
                lines = details_div.text.encode('utf-8').splitlines()
                showdate = datetime.strptime(lines[1], SERIES_PAGE_DATE_FORMAT)
                movie.showdate = datetime.strftime(showdate.replace(year=2018), Movie.DATE_FORMAT)
                for time_str in re.findall('\d+:\d+', lines[2]):
                    movie.addShowTime(movie.showdate, time_str.strip())
            # add movie to the list
            print movie
            movies.append(movie)

    movies_merged = mergeMovies(movies)
    PickleManager.dump(series_name, movies_merged)

    return movies_merged

def mergeMovies(movies):
    seen_titles = []
    movies_deduplicated = []
    for movie in movies:
        if movie.title not in seen_titles:
            new_movie = copy.deepcopy(movie)
            for similar in movies:
                if similar.title == movie.title and similar is not movie:
                    new_movie.showtimes.extend(similar.showtimes)
            movies_deduplicated.append(new_movie)
            seen_titles.append(movie.title)

    return movies_deduplicated

def getMoviesByDate(input_date):
    date = datetime.strptime(input_date, Movie.DATE_FORMAT)
    offset = date.date() - datetime.now().date()

    movies = []

    if offset.days > 6:
        raise ValueError('Cannot get movies for the day: {0}. Today is {1}'.format(date, today))
    else:
        soup = Common.getPageSoup(HOME_URL)
        for schedule in soup.find('div', {'id': 'tabs-{0}'.format(offset.days)}).findChildren(recursive=False):
            movie = createMovie(input_date, schedule)
            if movie is None:
                continue
            movies.append(movie)
        print 'Found {0} movies from {1} on {2}'.format(len(movies), FILM_FORUM_NAME, input_date)
        return movies


def main():
    reload(sys)
    sys.setdefaultencoding('utf8')

    # date = '2018-02-01'
    # movies = getMoviesByDate(date)
    # print movies

    # series_url = 'https://filmforum.org/series/ingmar-bergman-centennial-retrospective-series#now-playing'
    series_url = 'https://filmforum.org/series/michel-piccoli-series'
    print getMoviesBySeries('Michel Piccoli', series_url)


if __name__ == '__main__':
    main()