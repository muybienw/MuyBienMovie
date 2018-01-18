from Theaters import FilmForum
from Theaters import LincolnCenter
from Theaters import Metrograph
from Theaters import Quad
from Theaters import IFC
from Theaters import IMDB
from functools import partial

from time import sleep

import Douban
import Filter
import GoogleCalendar
import Config

import sys
import copy

EXPLORE_METHODS = {
    Config.FILM_FORUM: lambda x : FilmForum.getMoviesByDate(x),
    Config.ELINOR: LincolnCenter.getMoviesByDate,
    Config.WALTER_READE: LincolnCenter.getMoviesByDate,
    Config.QUAD: Quad.getMoviesByDate,
    Config.IFC: IFC.getMoviesByDate,
    Config.METROGRAPH: Metrograph.getMoviesByDate,
    Config.CINEPOLIS: partial(IMDB.getMoviesByDate, Config.CINEPOLIS),
    Config.ANGELIKA: partial(IMDB.getMoviesByDate, Config.ANGELIKA),
    Config.VILLAGE_EAST: partial(IMDB.getMoviesByDate, Config.VILLAGE_EAST),
    # Config.AMC25: lambda x: IMDB.getMoviesByDate(Config.AMC25, x),
    Config.AMC25: partial(IMDB.getMoviesByDate, Config.AMC25),
}

def exlporeMovieByDate(date):
    config = Config.getConfig(date)
    theaters = copy.deepcopy(config['theaters'])

    if Config.ELINOR in theaters and Config.WALTER_READE in theaters:
        theaters.remove(Config.ELINOR)

    for theater in theaters:
        print 'Exploring {0}...'.format(theater)
        exploreByTheater(EXPLORE_METHODS[theater](date))
        print '{0}: Done'.format(theater)
        sleep(60)

    # Step 1: get movies by theater
    # if Config.FILM_FORUM in theaters:
    #     exploreByTheater(Config.FILM_FORUM, FilmForum.getMoviesByDate(date))
    # if Config.ELINOR in theaters or Config.WALTER_READE in theaters:
    #     exploreByTheater('Lincoln Center', LincolnCenter.getMoviesByDate(date))
    # sleep(60)
    #
    # if Config.QUAD in theaters:
    #     exploreByTheater(Config.QUAD, Quad.getMoviesByDate(date))
    # if Config.IFC in theaters:
    #     exploreByTheater(Config.IFC, IFC.getMoviesByDate(date))
    # sleep(60)
    #
    # if Config.CINEPOLIS in theaters:
    #     exploreByTheater(Config.CINEPOLIS, IMDB.getMoviesByDate(Config.CINEPOLIS, date))
    # if Config.ANGELIKA in theaters:
    #     exploreByTheater(Config.ANGELIKA, IMDB.getMoviesByDate(Config.ANGELIKA, date))
    # sleep(60)
    #
    # if Config.METROGRAPH in theaters:
    #     exploreByTheater(Config.METROGRAPH, Metrograph.getMoviesByDate(date))
    # if Config.VILLAGE_EAST in theaters:
    #     exploreByTheater(Config.VILLAGE_EAST, IMDB.getMoviesByDate(Config.VILLAGE_EAST, date))
    # sleep(60)
    #
    # if Config.AMC25 in theaters:
    #     exploreByTheater(Config.AMC25, IMDB.getMoviesByDate(Config.AMC25, date))
    # sleep(30)

def exploreByTheater(movies):
    # Step 2: query Douban and fill in information
    for movie in movies:
        Douban.fillMovieInfo(movie)

    # Step 3: filter movies and
    # Step 4: put qualified movie on calendar
    for movie in Filter.filterMovies(movies):
        GoogleCalendar.putMovieOnCalendar(movie)

def main():
    reload(sys)
    sys.setdefaultencoding('utf8')

    date = '2018-01-18'
    GoogleCalendar.deleteAllEventsByDate(date)
    exlporeMovieByDate(date)


if __name__ == '__main__':
    main()

