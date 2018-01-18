#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup

import requests

from datetime import datetime

import Common
import Movie
import re

# the date field is in ISO format %Y-%d-%d
HOME_PAGE_URL = 'https://www.amctheatres.com/movie-theatres/new-york-city/amc-empire-25/showtimes/all/{date}/amc-empire-25/all'

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
    for detail_li in details_soup.find('ul', {'class': 'film-details'}).findChildren(recursive=False):
        label = detail_li.find('strong').text
        if label.lower() == 'year':
            movie.year = re.sub('year', '', detail_li.text, flags=re.IGNORECASE).strip()
        if label.lower() == 'director':
            movie.addDirectors(re.sub('director', '', detail_li.text, flags=re.IGNORECASE).strip())

    return movie

def getMoviesByDate(input_date):
    soup = Common.getPageSoup(HOME_PAGE_URL.format(date=input_date))
    print soup

    movies = []
    #
    # for movie_soup in Common.getPageSoup(HOME_PAGE_URL).find('div', {'class': ['daily-schedule', week_day_name]})\
    #         .find('ul').findChildren(recursive=False):
    #     movies.append(parseMovie(input_date, movie_soup))

    print 'Found {0} movies from {1} on {2}'.format(len(movies), 'AMC Empire 25', input_date)
    return movies

def getShowTimes():
    headers = {'X-AMC-Vendor-Key': '31dd5ae1-9562-4b1f-b718-f8b1a3a97492'}
    url = 'https://api.amctheatres.com//v2/theatres/42/showtimes'

    r = requests.get(url, headers=headers)
    print r


def main():
    getShowTimes()


if __name__ == '__main__':
    main()