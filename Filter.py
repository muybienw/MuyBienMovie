import Movie
import sys
import Config

# return the list of black-listed movie
def getMovieBlackListSet():
    with open(sys.path[0] + '/HaveSeenMovies.txt') as f:
        return set(map(str.lower, map(str.strip, f.readlines())))

def makeHaveSeenFilter(blacklist):
    def haveSeenFilter(movie):
        return movie.title.lower() not in blacklist
    return haveSeenFilter

def byDoubanRating(movie):
    result = True
    if movie.douban_rating is None:
        print 'No douban rating for movie: {0}({1})'.format(movie.title, movie.show_url)

    return movie.douban_rating is not None and movie.douban_rating >= Config.DOUBAN_RATING_BOUND

def filterShowTimes(movie):
    config = Config.getConfig(movie.showdate)

    available_showtimes = []
    for showtime in movie.showtimes:
        if config['start'] <= showtime.time() and showtime.time() <= config['end']:
                available_showtimes.append(showtime)
    movie.showtimes = available_showtimes
    return movie

def byAvailableTime(movie):
    return len(movie.showtimes) > 0

def filterMovies(movies):
    movies = filter(byDoubanRating, movies)
    # movies = filter(byAvailableTime, map(filterShowTimes, movies))
    # movies = filter(makeHaveSeenFilter(getMovieBlackListSet()), movies)   # Filtered in the explore module

    return movies

def main():
    movie = Movie.Movie()
    movie.title = 'The Square'
    movie_2 = Movie.Movie()
    movie_2.title = '9'
    movie_3 = Movie.Movie()
    movie_3.title = 'my Neighbor Totoro'
    movies = [movie, movie_2, movie_3]

    print filter(makeHaveSeenFilter(getMovieBlackListSet()), movies)

if __name__ == '__main__':
    main()