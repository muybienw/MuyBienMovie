#-*- coding: utf-8 -*-

import re
import Common
import Movie
import Config

FILM_PAGE_PREFIX = 'http://www.imdb.com/title/'

THEATERS = {
    Config.AMC25: {
        'imdb_url': 'http://www.imdb.com/showtimes/cinema/US/ci0010613/{0}',
        'full_name': 'AMC Empire 25',
    },
    Config.ANGELIKA: {
        'imdb_url': 'http://www.imdb.com/showtimes/cinema/US/ci0003467/{0}',
        'full_name': 'Angelika Film Center New York',
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

    # directors
    if url is not None:
        movie_page_soup = Common.getPageSoup(movie.show_url)
        if movie_page_soup is not None:
            for director_a in movie_page_soup.find('span', {'itemprop': 'director'}).find_all('span', {'itemprop': 'name'}):
                movie.addDirectors(director_a.text)

    # rating
    rating = movie_div.find('strong', {'itemprop': 'ratingValue'})
    if rating is not None:
     movie.imdb_rating = rating.text

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
    return movies

def main():
    date = '2018-01-19'
    getMoviesByDate(Config.CINEPOLIS, date)

if __name__ == '__main__':
    main()