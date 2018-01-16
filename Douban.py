# -*- coding: utf-8 -*-

import urllib
import urllib2
import json

def searchMovie(title):
    request = urllib2.Request('http://api.douban.com/v2/movie/search?' + urllib.urlencode({'q': title.encode('utf-8')}))

    try: response = urllib2.urlopen(request)
    except urllib2.URLError as e:
        print e.reason
        print e.read()
        return None

    movies = json.load(response)

    # returns the first search result
    if len(movies['subjects']) > 0:
        return movies['subjects'][0]
    else:
        print '''[Error]: Cannot find info for movie "{0}" on Douban'''.format(title)

def fillMovieInfo(movie):
    result = searchMovie(movie.title)

    if result is not None:
        movie.douban_rating = result['rating']['average']
        movie.douban_url = result['alt']

def main():
    # main code starts here

    # movie_title = 'city lights'
    # movie_title = 'spirited away'

    # movie_title = 'close-up'
    movie_title = 'Loving Vincent'
    print searchMovie(movie_title)

if __name__ == '__main__':
    main()