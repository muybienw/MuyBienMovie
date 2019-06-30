from datetime import datetime
import Common
import Movie

CALENDAR_URL = 'https://www.filmlinc.org/calendar/'
DIRECTOR_DELIMINATORS = '&|,|and'

def parseMovie(input_date, movie_info_soup):
    movie = Movie.Movie()
    movie.showdate = input_date
    title_info = movie_info_soup.find('h3').find('a')
    movie.title = title_info.text
    movie.show_url = title_info['href']

    for showtime_li in movie_info_soup.find('ul', {'class': 'co-showtimes-list'}).findChildren(recursive=False):
        movie.addShowTime(input_date, showtime_li.find('a').text)

    movie_page_soup = Common.getPageSoup(movie.show_url)
    movie_metadata_lis = movie_page_soup.find('div', {'class': 'film-meta'}).find('ul').findChildren(recursive=False)
    if len(movie_metadata_lis) >= 2:
        movie.addDirectors(movie_metadata_lis[0].text)
        movie.year = movie_metadata_lis[1].text

    # Venue info
    movie.theater = movie_page_soup.find('div', {'class': 'venue'}).find('a').text
    return movie

# input must be in %m/%d/%y format
def getMoviesByDate(input_date):
    date = datetime.strptime(input_date, Movie.DATE_FORMAT)
    day_str = str(date.month) if len(str(date.month)) == 2 else '0' + str(date.month)
    month_str = str(date.day) if len(str(date.day)) == 2 else '0' + str(date.day)
    year_str = str(date.year)[2:]
    tabId = day_str + month_str + year_str

    movies = []

    soup = Common.getPageSoup(CALENDAR_URL)
    daily_schedule = soup.find('li', {'id': tabId})

    if daily_schedule == None:
        print 'No movie schedule on {0} for Lincoln Center'.format(input_date)
    else:
        for film in daily_schedule.find_all('div', {'class': 'films'}):
            movies.append(parseMovie(input_date, film))
        print 'Found {0} movies from {1} on {2}'.format(len(movies), 'Lincoln Center', input_date)

    return movies

def main():
    input_date = '2019-07-05'
    print getMoviesByDate(input_date)


if __name__ == '__main__':
    main()