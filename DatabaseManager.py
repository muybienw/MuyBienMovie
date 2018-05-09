# -*- coding: utf-8 -*-

from pymongo import MongoClient

CLIENT = MongoClient()
MOVIE_DB = CLIENT.client.movie

import Movie

# Updates or creates a new movie entry in the database.
def addMovie(movie):
    if movie is None:
        '[Error] writing a movie == None to database'

    result = MOVIE_DB.insert_one(movie.__dict__)
    # print 'Inserted one movie successfully: {0}'.format(result.inserted_id)

# Searches and returns a movie object. Returns None if no match found.
def getMovie(movie):
    query = {'title': movie.title}
    results = MOVIE_DB.find(query)

    for result in results:
        if result['year'] == movie.year:
            return result

    return None

def removeAll():
    MOVIE_DB.remove()

def main():
    # movie = Movie.Movie()
    # movie.setTitle('MEMORIES OF UNDERDEVELOPMENT')
    # # movie.year = '2017'
    #
    # # addMovie(movie)
    # getMovie(movie)

    removeAll()

    # movie = Movie.Movie()
    # movie.setTitle('MEMORIES OF UNDERDEVELOPMENT')
    #
    # print getMovie(movie)

if __name__ == '__main__':
    main()