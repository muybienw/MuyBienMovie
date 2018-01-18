# -*- coding: utf-8 -*-

import re
from datetime import datetime

DATE_FORMAT = '%Y-%m-%d'
DIRECTOR_DELIMINATORS = '&|,| and '
TITLE_EXTRAS = ''': Director’s Cut|: Director's Cut|: The Director's Cut|: The Director’s Cut'''

class Movie:
    def __init__(self):
        self.title = ''
        self.directors = []
        self.showdate = None  # string in DATE_FORMAT
        self.theater = None
        self.showtimes = []
        self.douban_rating = None
        self.imdb_rating = None
        self.douban_url = None
        self.year = None
        self.description = None
        self.show_url = None
        self.length = None

    def __repr__(self):
        info = '{'
        if self.title:
            info += 'title: ' + self.title + '\n'
        if self.directors:
            info += 'directors: ' + str(self.directors) + '\n'
        if self.theater:
            info += 'theater: ' + str(self.theater) + '\n'
        if self.showdate:
            info += 'showdate: ' + str(self.showdate) + '\n'
        if self.showtimes:
            info += 'showtimes: ' + str(self.showtimes) + '\n'
        if self.douban_rating:
            info += 'douban_rating: ' + str(self.douban_rating) + '\n'
        if self.imdb_rating:
            info += 'imdb_rating: ' + str(self.imdb_rating) + '\n'
        if self.douban_url:
            info += 'douban_url: ' + self.douban_url + '\n'
        if self.year:
            info += 'year: ' + self.year + '\n'
        if self.description:
            info += 'description: ' + self.description + '\n'
        if self.show_url:
            info += 'show_url: ' + str(self.show_url) + '\n'
        if self.length:
            info += 'length: ' + self.length + '\n'

        info += '}'
        return info

    def __str__(self):
        info = ''
        if self.title:
            info += 'title: ' + self.title + '\n'
        if self.directors:
            info += 'directors: ' + str(self.directors) + '\n'
        if self.theater:
            info += 'theater: ' + str(self.theater) + '\n'
        if self.showdate:
            info += 'showdate: ' + str(self.showdate) + '\n'
        if self.showtimes:
            info += 'showtimes: ' + str(self.showtimes) + '\n'
        if self.douban_rating:
            info += 'douban_rating: ' + str(self.douban_rating) + '\n'
        if self.imdb_rating:
            info += 'imdb_rating: ' + str(self.imdb_rating) + '\n'
        if self.douban_url:
            info += 'douban_url: ' + self.douban_url + '\n'
        if self.year:
            info += 'year: ' + self.year + '\n'
        if self.description:
            info += 'description: ' + self.description + '\n'
        if self.show_url:
            info += 'show_url: ' + str(self.show_url) + '\n'
        if self.length:
            info += 'length: ' + self.length + '\n'

        return info

    def addShowTime(self, showdate_str, showtime_str):
        showtime_trimmed_str = re.search('(\d+):(\d+)', showtime_str)
        if showtime_trimmed_str is None:
            print ('invalid show time input: ' + showtime_str)
        else:
            showdatetime = showdate_str + ' ' + showtime_trimmed_str.group(0)
            if 'am' in showtime_str.lower():
                self.showtimes.append(datetime.strptime(showdatetime + ' AM', DATE_FORMAT + ' %I:%M %p'))
            else:
                self.showtimes.append(datetime.strptime(showdatetime + ' PM', DATE_FORMAT + ' %I:%M %p'))


    def addDirectors(self, directors_str):
        for director in re.split(DIRECTOR_DELIMINATORS, directors_str.lower().strip()):
            self.directors.append(director.encode('utf-8').strip())

    def setTitle(self, title_str):
        self.title = re.sub(TITLE_EXTRAS, '', title_str, flags=re.IGNORECASE)

def main():
    title = '1776: Director’s Cut'
    # print movie.title


if __name__ == '__main__':
    main()