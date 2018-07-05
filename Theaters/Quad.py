from datetime import datetime

import Common
import Movie

HOME_PAGE_URL = 'https://quadcinema.com/'

def parseMovie(input_date, movie_soup):
    movie = Movie.Movie()
    movie.showdate = input_date

    # title and show link
    title_info = movie_soup.find('h4')
    movie.show_url = title_info.a['href']
    movie.setTitle(title_info.a.text.encode('utf-8'))
    movie.theater = 'Quad Cinema'

    # # showtime
    for showtime_li in movie_soup.find('ul', {'class': 'showtimes-list'}).findChildren(recursive=False):
        movie.addShowTime(movie.showdate, showtime_li.a.text.replace('.', ':'))

    # director, year (hard to find this one)
    details_soup = Common.getPageSoup(movie.show_url)
    credit_name = details_soup.find('span', {'class': 'credit-name'})
    if credit_name is not None:
        movie.addDirectors(credit_name.text)

    return movie


def getMoviesByDate(input_date):
    date = datetime.strptime(input_date, Movie.DATE_FORMAT)
    offset = date.date() - datetime.now().date()

    if offset.days > 6:
        print 'Cannot get movies more than a week later: ' + input_date

    tabClass = 'date-' + (str(date.day) if date.day > 9 else '0' + str(date.day))

    movies = []

    for movie_soup in Common.getPageSoup(HOME_PAGE_URL).find('div', {'class': tabClass}).find_all('div', {'class': 'grid-item'}):
        movies.append(parseMovie(input_date, movie_soup))

    print 'Found {0} movies from {1} on {2}'.format(len(movies), 'Quad Cinema', input_date)
    return movies

def main():
    date = '2018-07-01'
    print getMoviesByDate(date)


if __name__ == '__main__':
    main()