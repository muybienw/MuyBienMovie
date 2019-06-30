from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from datetime import timedelta
from datetime import datetime
import Movie

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'google_calendar_client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-credentials.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def list_events():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

def putMovieOnCalendar():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    event = {
        'summary': 'A great film!',
        'location': 'Film Forum',
        'description': 'A great film is on the big screen!',
        'start': {
            'dateTime': '2018-01-07T09:00:00-07:00',
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': '2018-01-07T17:00:00-07:00',
            'timeZone': 'America/New_York',
        },
        'attendees': [
            {'email': 'mubin.w@gmail.com'},
        ],
    }

    response = service.events().insert(calendarId='primary', body=event).execute()

def putMovieOnCalendar(movie):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    summary = movie.title if movie.imdb_rating > 0 else '[?] ' + movie.title

    for showtime in movie.showtimes:
        endtime = showtime + timedelta(hours=2)
        event = {
            'summary': summary,
            'location': movie.theater,
            'description': presentMovie(movie),
            'start': {
                'dateTime': showtime.isoformat(),
                'timeZone': 'America/New_York',
            },
            'end': {
                'dateTime': endtime.isoformat(),
                'timeZone': 'America/New_York',
            },
            'attendees': [
                # {'email': 'mubin.w@gmail.com'},
            ],
        }

        if movie.imdb_rating >= 8.0:
            event['colorId'] = '6'  # red
        elif movie.imdb_rating >= 7.5:
            event['colorId'] = '5'  # orange

        response = service.events().insert(calendarId='primary', body=event).execute()

def putMovieOnSpecificCalendar(movie, calendarId):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    # prepare the calendar event
    summary = movie.title if movie.imdb_rating > 0 else '[?] ' + movie.title

    for i in xrange(len(movie.showtimes)):
        showtime = movie.showtimes[i]
        endtime = showtime + timedelta(hours=2)
        event = {
            'summary': summary,
            'location': movie.theater,
            'description': presentMovie(movie),
            'start': {
                'dateTime': showtime.isoformat(),
                'timeZone': 'America/New_York',
            },
            'end': {
                'dateTime': endtime.isoformat(),
                'timeZone': 'America/New_York',
            },
            'attendees': [
                # {'email': 'mubin.w@gmail.com'},
            ],
        }
        if movie.imdb_rating >= 8.0:
            event['colorId'] = '6'  # red
        elif movie.imdb_rating >= 7.5:
            event['colorId'] = '5'  # orange

        if i == len(movie.showtimes) - 1:
            event['summary'] = '[!]' + event['summary']

        response = service.events().insert(calendarId=calendarId, body=event).execute()


# return the calendar id: clears the original and makes a new calendar
def updateCalendarByName(calendarName):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    calendarId = getCalendarIdByName(service, calendarName)

    # clear existing calendar
    if calendarId is not None:
        service.calendars().delete(calendarId=calendarId).execute()

    # create new calendar for series
    calendar = {
        'summary': calendarName,
        'timeZone': 'America/New_York'
    }
    created_calendar = service.calendars().insert(body=calendar).execute()
    return created_calendar['id']


def getCalendarIdByName(service, calendarName):
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            if calendar_list_entry['summary'] == calendarName:
                return calendar_list_entry['id']
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

    return None

def presentMovie(movie):
    return str(movie)

def create_movie_event():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    event = {
        'summary': 'A great film!',
        'location': 'Film Forum',
        'description': 'A great film is on the big screen!',
        'start': {
            'dateTime': '2018-01-07T09:00:00-05:00',
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': '2018-01-07T17:00:00-05:00',
            'timeZone': 'America/New_York',
        },
        'attendees': [
            {'email': 'mubin.w@gmail.com'},
        ],
    }

    response = service.events().insert(calendarId='primary', body=event).execute()

def listAllEventsByDate(date):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    timeMax = date + 'T23:59:59-05:00'
    timeMin = date + 'T00:00:00-05:00'
    timeZone = 'America/New_York'

    events = []

    page_token = None
    while True:
        response = service.events().list(calendarId='primary', pageToken=page_token,\
                                       timeMax=timeMax, timeMin=timeMin, timeZone=timeZone).execute()
        events.extend(response['items'])
        page_token = response.get('nextPageToken')
        if not page_token:
            break

    return events

def deleteEvent(id):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    service.events().delete(calendarId='primary', eventId=id).execute()

def deleteAllEventsByDate(date):
    events = listAllEventsByDate(date)
    print('Found {0} events on {1}, deleting...'.format(len(events), date))
    for event in events:
        deleteEvent(event['id'])
    print('All events deleted.'.format(len(events), date))

def main():
    date = '2018-01-13'
    putMovieOnSpecificCalendar(None, 'haha')

if __name__ == '__main__':
    main()