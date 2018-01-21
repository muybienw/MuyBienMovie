from datetime import datetime
import re
import Common
import Movie

HOME_PAGE_URL = 'http://metrograph.com/'
MOVIE_URL_PREFIX = 'http://metrograph.com/film/'
SCHEDULE_PREFIX = 'http://metrograph.com/film?d='

def parseMovie(input_date, movie_soup):
    movie = Movie.Movie()
    movie.showdate = input_date
    movie.theater = 'Metrograph'

    # title and show link
    title_info = movie_soup.find('h4')
    movie.title = title_info.a.text
    movie.show_url = title_info.a['href']

    # showtime
    for showtime_a in movie_soup.find('div', {'class': 'showtimes'}).find_all('a'):
        movie.addShowTime(movie.showdate, showtime_a.text)

    # director, year
    details_soup = movie_soup.find('div', {'class': 'details'})
    if details_soup is None:
        print 'Cannot find movie details for: {0}'.format(movie.title)
    match = re.search('director:(.*)(\d{4}) /', details_soup.text, flags=re.IGNORECASE)
    movie.addDirectors(match.group(1))
    movie.year = match.group(2)

    return movie


def getMoviesByDate(input_date):
    date = datetime.strptime(input_date, Movie.DATE_FORMAT)
    today = date.today()
    offset = date.day - today.day

    if offset > 6:
        print 'Cannot get movies more than a week later: ' + input_date

    movies = []

    soup = Common.getPageSoup('http://metrograph.com/film?d=' + input_date)

    if soup is None:
        print 'Cannot find movie for Metrograph on {0}'.format(input_date)
        return movies

    for movie_div in soup.find_all('div', {'class': 'film'}):
        if movie_div is not None:
            movies.append(parseMovie(input_date, movie_div))

    print 'Found {0} movies from {1} on {2}'.format(len(movies), 'Metrograph', input_date)
    return movies

def main():
    date = '2018-01-20'
    print getMoviesByDate(date)


if __name__ == '__main__':
    main()