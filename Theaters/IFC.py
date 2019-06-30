#-*- coding: utf-8 -*-

from datetime import datetime

import Common
import Movie
import re

HOME_PAGE_URL = 'http://www.ifccenter.com/'

def parseMovie(input_date, movie_soup):
    movie = Movie.Movie()
    movie.showdate = input_date

    # title and show link
    title_info = movie_soup.find('div', {'class': 'details'}).find('h3')

    movie.show_url = title_info.a['href']
    movie.setTitle(title_info.a.text.encode('utf-8'))
    movie.theater = 'IFC'

    # showtime
    for showtime_li in movie_soup.find('ul', {'class': 'times'}).findChildren(recursive=False):
        movie.addShowTime(movie.showdate, showtime_li.a.text)

    # director, year (hard to find this one)
    details_soup = Common.getPageSoup(movie.show_url)
    details = details_soup.find('ul', {'class': 'film-details'})
    if details is not None:
        for detail_li in details.findChildren(recursive=False):
            label = detail_li.find('strong').text
            if label.lower() == 'year':
                movie.year = re.sub('year', '', detail_li.text, flags=re.IGNORECASE).strip()
            if label.lower() == 'director':
                movie.addDirectors(re.sub('director', '', detail_li.text, flags=re.IGNORECASE).strip())
    else:
        print 'This doesn\'t look like a movie: {0}({1})'.format(movie.title, movie.show_url)
    return movie

def getMoviesByDate(input_date):
    date = datetime.strptime(input_date, Movie.DATE_FORMAT)
    today = date.today()
    delta = date.date() - today.date()
    offset = delta.days

    if offset > 6:
        print 'Cannot get movies more than a week later: ' + input_date

    week_day_name = str(date.strftime('%a')).lower()

    movies = []

    for movie_soup in Common.getPageSoup(HOME_PAGE_URL).find('div', {'class': week_day_name})\
            .find('ul').findChildren(recursive=False):
        try:
            movie = parseMovie(input_date, movie_soup)
            movies.append(movie)
        except TypeError:
            print 'Parse movie error'

    print 'Found {0} movies from {1} on {2}'.format(len(movies), 'IFC', input_date)
    return movies

def main():
    date = '2019-07-04'
    print getMoviesByDate(date)


if __name__ == '__main__':
    main()