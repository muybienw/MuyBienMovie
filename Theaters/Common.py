from bs4 import BeautifulSoup

import requests

# return the soup
def getPageSoup(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

    r = requests.get(url, headers=headers)
    return BeautifulSoup(r.text, 'html.parser')

def main():
    # url = 'https://www.amctheatres.com/movie-theatres/new-york-city/amc-empire-25/showtimes/all/2018-01-16/amc-empire-25/all'
    url = 'http://www.imdb.com/showtimes/cinema/US/ci0010613?ref_=shlc_tny_th'
    print getPageSoup(url)

if __name__ == '__main__':
    main()