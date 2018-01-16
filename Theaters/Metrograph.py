from datetime import datetime
import re
import Common
import Movie

HOME_PAGE_URL = 'http://metrograph.com/'
MOVIE_URL_PREFIX = 'http://metrograph.com/film/'

def parseMovie(input_date, movie_soup):
    movie = Movie.Movie()
    movie.showdate = input_date

    # title and show link
    title_info = movie_soup.find('span', {'class': 'title'})
    if not title_info.a['href'].startswith(MOVIE_URL_PREFIX):
        return None  # this is not a movie page
    movie.show_url = title_info.a['href']
    movie.title = title_info.a.text
    movie.theater = 'Metrograph'

    # showtime
    for showtime_a in movie_soup.find('span', {'class': 'showtimes'}).find_all('a'):
        movie.addShowTime(movie.showdate, showtime_a.text)

    # director, year
    details_soup = Common.getPageSoup(movie.show_url).find('div', {'class': 'details'})
    movie.year_soup = details_soup.find('div', {'class': 'specs'}).text.split('/')[0].strip()

    for line in re.split('\\t', details_soup.text):
        if 'director' in line.lower():
            movie.addDirectors(line.lower().split('director:')[1])

    return movie


def getMoviesByDate(input_date):
    date = datetime.strptime(input_date, Movie.DATE_FORMAT)
    today = date.today()
    offset = date.day - today.day

    if offset > 6:
        print 'Cannot get movies more than a week later: ' + input_date
    tabId = 'day-offset-' + str(offset)

    movies = []

    for movie_soup in Common.getPageSoup(HOME_PAGE_URL).find('div', {'id': tabId}).find_all('li'):
        movie = parseMovie(input_date, movie_soup)
        if movie is not None:
            movies.append(parseMovie(input_date, movie_soup))

    print 'Found {0} movies from {1} on {2}'.format(len(movies), 'Metrograph', input_date)
    return movies

def main():
    date = '2018-01-14'
    print getMoviesByDate(date)


if __name__ == '__main__':
    main()