#-*- coding: utf-8 -*-

import re
import Common
import Movie
import Config

import requests

HOME_PREFIX = 'http://www.imdb.com/'
FILM_PAGE_PREFIX = 'http://www.imdb.com/title/'
SEARCH_PREFIX = 'http://www.imdb.com/find'

OMDB_KEY = '9e865ca2' # registered with 523219531@qq.com
OMDB_URL = 'http://www.omdbapi.com/'

THEATERS = {
    Config.AMC25: {
        'imdb_url': 'http://www.imdb.com/showtimes/cinema/US/ci0010613/{0}',
        'full_name': 'AMC Empire 25',
    },
    Config.AMC_LOWES_34: {
        'imdb_url': 'http://www.imdb.com/showtimes/cinema/US/ci0011588/{0}',
        'full_name': 'AMC Lowes 34',
    },
    Config.AMC_LINCOLN_SQUARE: {
        'imdb_url': 'http://www.imdb.com/showtimes/cinema/US/ci0001803/{0}',
        'full_name': 'AMC Loews Lincoln Square 13',
    },
    Config.ANGELIKA: {
        'imdb_url': 'http://www.imdb.com/showtimes/cinema/US/ci0003467/{0}',
        'full_name': 'Angelika Film Center New York',
    },
    Config.REGAL_UNION_SQUARE: {
        'imdb_url': 'http://www.imdb.com/showtimes/cinema/US/ci0007135/{0}',
        'full_name': 'Regal Union Square',
    },
    Config.CINEPOLIS: {
        'imdb_url': 'http://www.imdb.com/showtimes/cinema/US/ci41794468/{0}',
        'full_name': 'Cinépolis Chelsea',
    },
    Config.VILLAGE_EAST: {
        'imdb_url': 'http://www.imdb.com/showtimes/cinema/US/ci0003464/{0}',
        'full_name': 'City Cinemas Village East Cinema',
    },
    Config.QUAD: {
        'imdb_url': 'http://www.imdb.com/showtimes/cinema/US/ci0003552/{0}',
        'full_name': 'Quad Cinema',
    },
    Config.FILM_FORUM: {
        'imdb_url': 'http://www.imdb.com/showtimes/cinema/US/ci0003551/{0}',
        'full_name': 'Film Forum',
    },
    Config.WALTER_READE: {
        'imdb_url': 'http://www.imdb.com/showtimes/cinema/US/ci0003556/{0}',
        'full_name': 'Film Society Lincoln Center - Walter Reade Theater',
    },
    Config.IFC: {
        'imdb_url': 'http://www.imdb.com/showtimes/cinema/US/ci0013904/{0}',
        'full_name': 'IFC Center',
    },
    Config.ELINOR: {
        'imdb_url': 'http://www.imdb.com/showtimes/cinema/US/ci12617789/{0}',
        'full_name': 'Film Society Lincoln Center - Elinor Bunin Munroe Film Center',
    },
    Config.BAM: {
        'imdb_url': 'https://www.imdb.com/showtimes/cinema/US/ci0010119/{0}',
        'full_name': 'BAM Rose Cinemas',
    },
}

def parseMovie(theater_str, input_date, movie_div):
    movie = Movie.Movie()

    movie.showdate = input_date
    movie.theater = THEATERS[theater_str]['full_name']

    # title
    title_h3 = movie_div.find('div', {'class': 'info'}).find('h3')
    year_match = re.search('\((\d+)\)', title_h3.text)
    if year_match is None:
        movie.setTitle(title_h3.text)
    else:
        movie.setTitle(title_h3.text.split('(')[0].strip())
        movie.year = year_match.group(1)

    # url
    url = title_h3.find('a', {'itemprop': 'url'})
    if url is not None:
        movie.show_url = FILM_PAGE_PREFIX + re.search('tt\d+', url['href']).group(0)
        movie.imdb_url = movie.show_url

    # directors
    if url is not None:
        movie_page_soup = Common.getPageSoup(movie.show_url)
        if movie_page_soup is not None:
            director_span = movie_page_soup.find('span', {'itemprop': 'director'})
            if director_span is not None:
                for director_a in director_span.find_all('span', {'itemprop': 'name'}):
                    movie.addDirectors(director_a.text)

    # rating
    rating = movie_div.find('strong', {'itemprop': 'ratingValue'})
    if rating is not None and rating.text != '-':
        movie.imdb_rating = float(rating.text)

    # showtimes
    for showtime_a in movie_div.find('div', {'class': 'showtimes'}).find_all('a', {'rel': 'nofollow'}):
        movie.addShowTime(input_date, showtime_a.text)

    return movie

def getMoviesByDate(theater_str, input_date):
    if theater_str not in THEATERS:
        print 'Cannot find movies for theater: {0}'.format(theater_str)

    movies = []

    soup = Common.getPageSoup(THEATERS[theater_str]['imdb_url'].format(input_date))
    showtimes = soup.find('div', {'class': ['list', 'detail']})
    if showtimes is None:
        print 'Seems cannot find any movies for {0} on {1}'.format(theater_str, input_date)
        return movies

    for movie_div in showtimes.find_all('div', {'class': 'list_item'}):
        movies.append(parseMovie(theater_str, input_date, movie_div))

    print 'Found {0} movies from {1} on {2}'.format(len(movies), theater_str, input_date)
    return movies

def fillMovieInfo(movie):
    if not movie.title:
        print("Movie has not title, abort!")
        return movie
    movie_json = findMovieByTitleOmdb(movie.title.encode('utf-8'))

    if 'Error' in movie_json:
        print("Movie not found: " + movie.title)
        return movie

    movie.imdb_rating = float(movie_json['imdbRating']) if isFloat(movie_json['imdbRating']) else 0
    movie.imdb_id = movie_json['imdbID']
    movie.imdb_url = 'https://www.imdb.com/title/' + movie_json['imdbID']
    movie.addDirectors(movie_json['Director'])

    return movie

# Returns the imdb url
# This method is deprecated
def searchMoviePageByTitle(movie):
    payload = {'q': movie.title.encode('utf-8'), 's': 'tt'}
    soup = Common.getPageSoup(SEARCH_PREFIX, params=payload)

    if soup is None:
        return None

    for result in soup.find_all('td', {'class': 'result_text'}):
        match = re.match('(.*)\((\d{4})\)', result.text)
        if match is None:
            print '[Error][IMDB]: cannot parse the search result: {0}'.format(result.text)
            continue
        year = match.group(2)
        if year != movie.year and year != movie.douban_year:
            continue
        return HOME_PREFIX + result.a['href']

    print '[Error][IMDB]: no match for movie: {0}'.format(movie.title)
    return None


def findMovieByTitleOmdb(movie_title):
    print("Looking up info for movie title: " + movie_title)
    params = {'apikey': OMDB_KEY, 't': movie_title}
    response = requests.get(url=OMDB_URL, params=params)

    return response.json()

def isFloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def main():
    movie_json = findMovieByTitleOmdb('the chambermaid')
    print movie_json

if __name__ == '__main__':
    main()