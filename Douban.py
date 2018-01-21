# -*- coding: utf-8 -*-

import Movie
import requests

def searchMovie(title):
    payload = {'q': title.encode('utf-8')}
    response = requests.get('http://api.douban.com/v2/movie/search', params=payload)

    if response.status_code == 200:
        return response.json()['subjects']
    else:
        print '[Error][Douban] unable to search for query: {0}, error code: {1}'.format(response.url, response.status_code)

def fillMovieInfoWithSubject(movie, subject):
    movie.douban_rating = subject['rating']['average']
    movie.douban_url = subject['alt']
    movie.douban_year = subject['year']

def fillMovieInfo(movie):
    result = searchMovie(movie.title)

    if result is None or len(result) == 0:
        print '[Error][Douban] unable to find a match for {0}'.format(movie.title)
        return

    if movie.year is None:
        fillMovieInfoWithSubject(movie, result[0])  # the best hope
        return

    for subject in result:
        if subject['year'] == movie.year:
            fillMovieInfoWithSubject(movie, subject)
            return

    print '[Error][Douban] no match found for {0}, year: {1}'.format(movie.title, movie.year)

def main():
    movie = Movie.Movie()
    movie.title = 'happy end'
    movie.year = '1000'
    fillMovieInfo(movie)

    print str(movie)

if __name__ == '__main__':
    main()