from Theaters import FilmForum
from Theaters import LincolnCenter
from Theaters import Metrograph
from Theaters import Quad
from Theaters import IFC
from Theaters import IMDB
from functools import partial

from time import sleep
from datetime import datetime

import Douban
import Filter
import GoogleCalendar
import Config
import Movie
import DatabaseManager

import sys
import copy

EXPLORE_METHODS_LONG = {
    Config.FILM_FORUM: FilmForum.getMoviesByDate,
    Config.ELINOR: LincolnCenter.getMoviesByDate,
    Config.WALTER_READE: LincolnCenter.getMoviesByDate,
    Config.QUAD: Quad.getMoviesByDate,
    Config.IFC: IFC.getMoviesByDate,
    Config.METROGRAPH: Metrograph.getMoviesByDate,
    Config.CINEPOLIS: partial(IMDB.getMoviesByDate, Config.CINEPOLIS),
    Config.ANGELIKA: partial(IMDB.getMoviesByDate, Config.ANGELIKA),
    Config.VILLAGE_EAST: partial(IMDB.getMoviesByDate, Config.VILLAGE_EAST),
    Config.AMC25: partial(IMDB.getMoviesByDate, Config.AMC25),
}

EXPLORE_METHODS_SHORT = {
    Config.FILM_FORUM: partial(IMDB.getMoviesByDate, Config.FILM_FORUM),
    Config.ELINOR: partial(IMDB.getMoviesByDate, Config.ELINOR),
    Config.WALTER_READE: partial(IMDB.getMoviesByDate, Config.WALTER_READE),
    Config.QUAD: partial(IMDB.getMoviesByDate, Config.QUAD),
    Config.IFC: partial(IMDB.getMoviesByDate, Config.IFC),
    Config.METROGRAPH: Metrograph.getMoviesByDate,
    Config.CINEPOLIS: partial(IMDB.getMoviesByDate, Config.CINEPOLIS),
    Config.ANGELIKA: partial(IMDB.getMoviesByDate, Config.ANGELIKA),
    Config.VILLAGE_EAST: partial(IMDB.getMoviesByDate, Config.VILLAGE_EAST),
    Config.AMC25: partial(IMDB.getMoviesByDate, Config.AMC25),
}

HAVE_SEENS = Filter.makeHaveSeenFilter(Filter.getMovieBlackListSet())

def exlporeMovieByDate(date):
    config = Config.getConfig(date)
    theaters = copy.deepcopy(config['theaters'])

    # day_diff = datetime.strptime(date, Movie.DATE_FORMAT).date() - datetime.today().date()
    # methods = EXPLORE_METHODS_LONG
    # if day_diff.days < 0:
    #     print '[Error] no point exploring movies in the past!'
    # elif day_diff.days < 2:
    #     methods = EXPLORE_METHODS_SHORT
    # else:
    #     methods = EXPLORE_METHODS_LONG
    #     if Config.ELINOR in theaters and Config.WALTER_READE in theaters:
    #         theaters.remove(Config.ELINOR)

    methods = EXPLORE_METHODS_LONG
    if Config.ELINOR in theaters and Config.WALTER_READE in theaters:
        theaters.remove(Config.ELINOR)

    # override the theaters to explore
    # theaters = [Config.AMC25, Config.FILM_FORUM, Config.IFC, Config.QUAD, Config.WALTER_READE, Config.ELINOR]

    print "=== Date: {0}, Theaters: {1} ===".format(date, theaters)

    for theater in theaters:
        print 'Exploring {0}...'.format(theater)
        exploreByTheater(methods[theater](date))
        print '{0}: Done'.format(theater)
        # sleep(60)

def exploreByTheater(movies):
    # Step 1: remove have seen, time-not-available movies
    movies = filter(Filter.byAvailableTime, map(Filter.filterShowTimes, movies))
    movies = filter(HAVE_SEENS, movies)

    # Step 2: search over databse to avoid extra Douban/IMDB query
    movies_complete = []
    movies_incomplete = []
    for movie in movies:
        saved = DatabaseManager.getMovie(movie)
        if saved is None:
            movies_incomplete.append(movie)
        else:
            fillMovieInfoWithSavedMovie(movie, saved)
            movies_complete.append(movie)

    print 'complete movies #: {0}'.format(len(movies_complete))
    print 'incomplete movies #: {0}'.format(len(movies_incomplete))
    # Step 3: query Douban/IMDB to fill incomplete movies
    for movie in movies_incomplete:
        Douban.fillMovieInfo(movie)
        IMDB.fillMovieInfo(movie)
        DatabaseManager.addMovie(movie)
        movies_complete.append(movie)

    print movies_complete

    # Step 4: filter movies by Douban/IMDB related info
    # Step 5: put qualified movie on calendar
    for movie in filter(Filter.byRating, movies_complete):
        GoogleCalendar.putMovieOnCalendar(movie)


def fillMovieInfoWithSavedMovie(movie, saved):
    movie.douban_id = saved['douban_id']
    movie.douban_rating = saved['douban_rating']
    movie.douban_url = saved['douban_url']
    movie.douban_year = saved['douban_year']
    movie.imdb_url = saved['imdb_url']
    movie.imdb_rating = saved['imdb_rating']
    movie.imdb_year = saved['imdb_year']


def main():
    reload(sys)
    sys.setdefaultencoding('utf8')

    date = '2018-01-23'
    GoogleCalendar.deleteAllEventsByDate(date)
    exlporeMovieByDate(date)


if __name__ == '__main__':
    main()