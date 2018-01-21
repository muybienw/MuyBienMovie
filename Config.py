from datetime import datetime
from datetime import time

import Movie
import sys
import holidays

US_HOLIDAYS = holidays.UnitedStates()

DOUBAN_RATING_BOUND = 8.0

# isoweekday
MONDAY = 1
TUESDAY = 2
WEDNESDAY = 3
THURSDAY = 4
FRIDAY = 5
SATURDAY = 6
SUNDAY = 7
HOLIDAY = 8

AMC25 = 'AMC 25'
ANGELIKA = 'Angelika'
CINEPOLIS = 'Cinepolis'
VILLAGE_EAST = 'Village East'
QUAD = 'Quad'
FILM_FORUM = 'Film Forum'
WALTER_READE = 'Walter Reade'
IFC = 'IFC'
ELINOR = 'Elinor Bunin Munroe'
METROGRAPH = 'Metrograph'

THEATERS = {AMC25, ANGELIKA, CINEPOLIS, VILLAGE_EAST, QUAD, FILM_FORUM, WALTER_READE, IFC, ELINOR, METROGRAPH}

WEEKDAY_THEATERS = [AMC25, FILM_FORUM, IFC, QUAD, CINEPOLIS, WALTER_READE, ELINOR]
HOLIDAY_THEATERS = list(THEATERS)

CONFIG_BY_WEEKDAY = {
    MONDAY: {
        'theaters': WEEKDAY_THEATERS,
        'start': time(17),
        'end': time(20)
    },
    TUESDAY: {
        'theaters': WEEKDAY_THEATERS,
        'start': time(17),
        'end': time(20)
    },
    WEDNESDAY: {
        'theaters': WEEKDAY_THEATERS,
        'start': time(17),
        'end': time(20)
    },
    THURSDAY: {
        'theaters': WEEKDAY_THEATERS,
        'start': time(17),
        'end': time(20)
    },
    FRIDAY: {
        'theaters': WEEKDAY_THEATERS,
        'start': time(17),
        'end': time(20)
    },
    SATURDAY: {
        'theaters': HOLIDAY_THEATERS,
        'start': time(10),
        'end': time(21)
    },
    SUNDAY: {
        'theaters': HOLIDAY_THEATERS,
        'start': time(10),
        'end': time(20)
    },
    HOLIDAY: {
        'theaters': HOLIDAY_THEATERS,
        'start': time(10),
        'end': time(21)
    }
}

def getConfig(date):
    weekday = datetime.strptime(date, Movie.DATE_FORMAT).date().isoweekday()

    # override times for holiday
    if date in US_HOLIDAYS:
        weekday = HOLIDAY

    return CONFIG_BY_WEEKDAY[weekday]

def main():
    date = '2018-01-15'
    print getConfig(date)

if __name__ == '__main__':
    main()