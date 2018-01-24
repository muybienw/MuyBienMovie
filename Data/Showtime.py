# -*- coding: utf-8 -*-

import re
from datetime import datetime

class Showtime:
    def __init__(self):
        self.movie = None
        self.theater = None
        self.link = None
        self.time = None

    def __str__(self):
        print '{0}\n{1}\n{2}\n{3}\n'.format(self.movie, self.theater, self.link, self.time)

def main():
    print 'This is a showtime object!'


if __name__ == '__main__':
    main()