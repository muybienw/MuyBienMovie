from datetime import datetime
from datetime import time
from Movie import Movie

import Movie
import sys
import holidays

US_HOLIDAYS = holidays.UnitedStates()

DOUBAN_RATING_BOUND = 8.0

# isoweekday
MONDAY = 1
TUESDAY = 2
WEDNESDAY = 3
THURSDAY = 4
FRIDAY = 5
SATURDAY = 6
SUNDAY = 7
HOLIDAY = 8

AVAILABLE_HOURS_BY_WEEKDAY = {
    MONDAY: {
        'start': time(17),
        'end': time(20, 30)
    },
    TUESDAY: {
        'start': time(17),
        'end': time(20, 30)
    },
    WEDNESDAY: {
        'start': time(17),
        'end': time(20, 30)
    },
    THURSDAY: {
        'start': time(17),
        'end': time(20, 30)
    },
    FRIDAY: {
        'start': time(17),
        'end': time(20, 30)
    },
    SATURDAY: {
        'start': time(10),
        'end': time(21)
    },
    SUNDAY: {
        'start': time(10),
        'end': time(20)
    },
    HOLIDAY: {
        'start': time(10),
        'end': time(21)
    }
}

# return the list of black-listed movie
def getMovieBlackListSet():
    with open(sys.path[0] + '/HaveSeenMovies.txt') as f:
        return set(map(str.strip, f.readlines()))

def makeHaveSeenFilter(blacklist):
    def haveSeenFilter(movie):
        return movie.title.lower() not in blacklist
    return haveSeenFilter

def byDoubanRating(movie):
    return movie.douban_rating is not None and movie.douban_rating >= DOUBAN_RATING_BOUND

def filterShowTimes(movie):
    weekday = datetime.strptime(movie.showdate, Movie.DATE_FORMAT).date().isoweekday()

    # override times for holiday
    if movie.showdate in US_HOLIDAYS:
        weekday = HOLIDAY

    available_showtimes = []
    for showtime in movie.showtimes:
        if AVAILABLE_HOURS_BY_WEEKDAY[weekday]['start'] <= showtime.time() \
            and showtime.time() <= AVAILABLE_HOURS_BY_WEEKDAY[weekday]['end']:
                available_showtimes.append(showtime)
    movie.showtimes = available_showtimes
    return movie

def byAvailableTime(movie):
    return len(movie.showtimes) > 0

def filterMovies(movies):
    movies = filter(byAvailableTime, map(filterShowTimes, movies))
    movies = filter(makeHaveSeenFilter(getMovieBlackListSet()), movies)
    movies = filter(byDoubanRating, movies)

    return movies

def main():
    # movie = Movie()
    # movie.title = 'The Square'
    # movie_2 = Movie()
    # movie_2.title = '9'
    # movie_3 = Movie()
    # movie_3.title = 'A non-existing movie'
    # movies = [movie, movie_2, movie_3]

    us_holidays = holidays.UnitedStates()
    print '2018-01-15' in us_holidays

if __name__ == '__main__':
    main()