from Theaters import FilmForum
from Theaters import LincolnCenter
from Theaters import Metrograph
from Theaters import Quad
from Theaters import IFC

from time import sleep

import Douban
import Filter
import GoogleCalendar


import sys

def exlporeMovieByDate(date):
    # Step 1: get movies by theater
    exploreByTheater('Film Forum', FilmForum.getMoviesByDate(date))
    exploreByTheater('Lincoln Center', LincolnCenter.getMoviesByDate(date))
    sleep(60)  # wait for a minute to make Douban API happy (40 reqs/min)
    exploreByTheater('Metrograph', Metrograph.getMoviesByDate(date))
    exploreByTheater('Quad Cinema', Quad.getMoviesByDate(date))
    sleep(60)
    exploreByTheater('IFC', IFC.getMoviesByDate(date))

def exploreByTheater(theater_name, movies):
    print 'Exploring {0}...'.format(theater_name)
    # Step 2: query Douban and fill in information
    for movie in movies:
        Douban.fillMovieInfo(movie)

    # Step 3: filter movies and
    # Step 4: put qualified movie on calendar
    for movie in Filter.filterMovies(movies):
        GoogleCalendar.putMovieOnCalendar(movie)

    print '{0}: Done'.format(theater_name)

def main():
    reload(sys)
    sys.setdefaultencoding('utf8')

    date = '2018-01-17'
    GoogleCalendar.deleteAllEventsByDate(date)
    exlporeMovieByDate(date)


if __name__ == '__main__':
    main()

