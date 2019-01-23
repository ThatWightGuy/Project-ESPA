from requests import get
from requests.exceptions import RequestException
from bs4 import BeautifulSoup as bs
from contextlib import closing
import webbrowser as wb

DEFAULT_PATH = "https://www.imdb.com"
URL_ADDON = {'TITLE': '/title/',  # For the specific title page
             'NAME': '/name/',  # For the specific person page
             'SEARCH': '/search/',  # For when making search queries
             'TITLE_QUERY': 'title?',  # This is always put before the rest of the tile search filters
             'TITLE_SEARCH': 'title=',  # Searching for a title by name or keyword
             'TITLE_TYPE': 'title_type=',  # Noting what kind of title we are searching for (will always be feature)
             'RELEASE_DATE': 'release_date=',  # Use a comma to denote a time period (ex 01-01-1998, 01-01-1999)
             'GENRE_SEARCH': 'genres=',  # This too uses a comma to delimit multiple genres
             'NAME_QUERY': 'name?',  # This is always put before the rest of the name search filters
             'NAME_SEARCH': 'name=',  # Searching for a name
             'PAGE_VIEW': 'view='  # should always be 'simple'
             }  # Filters for different page criteria


def get_url_content(url):
    try:
        with closing(get(url, stream=True)) as response:
            if checkResponse(response):
                return response.content

    except RequestException as e:
        print(str(e))
        return ''


def checkResponse(response):
    goodResponse = False
    if response.status_code == 200:
        goodResponse = True

    return goodResponse


class Search:
    def __init__(self):
        self.searchURL = str()

    def getInitTitleSearchURL(self):
        return DEFAULT_PATH + URL_ADDON['SEARCH'] + URL_ADDON['TITLE_QUERY']

    def getInitNameSearchURL(self):
        return DEFAULT_PATH + URL_ADDON['SEARCH'] + URL_ADDON['NAME_QUERY']

    def setInitTitleSearchURL(self):
        self.searchURL = self.getInitTitleSearchURL()

    def setInitNameSearchURL(self):
        self.searchURL = self.getInitNameSearchURL()

    def insertURLAddon(self, addonType, addonVal):
        self.searchURL += "&" + URL_ADDON[addonType] + addonVal

    def getSearchURL(self):
        return self.searchURL

    def getSearches(self):
        searchList = list()
        urlContent = get_url_content(self.getSearchURL())

        if urlContent != '' and self.getSearchURL() != self.getInitTitleSearchURL():
            html = bs(urlContent, 'html.parser')
            rawList = html.find_all('div', class_='lister-item mode-advanced')

            if self.getInitNameSearchURL() in self.getSearchURL():
                rawList = html.find_all('div', class_='lister-item mode-detail')

            # To minimize time spent parsing info, number of list items will be reduced to 5
            listRange = 5

            if len(rawList) < listRange:
                listRange = len(rawList)

            for listItem in range(listRange):
                searchInfo = list()

                name = str(rawList[listItem].h3.a.text).lstrip().replace("\n", '')
                searchInfo.append(name)

                if self.getInitTitleSearchURL() in self.getSearchURL():
                    searchInfo.append(rawList[listItem].find('span', class_='lister-item-year text-muted unbold').text)

                searchInfo.append(str(DEFAULT_PATH + rawList[listItem].a['href']))
                searchList.append(searchInfo)

        else:
            print('Bad Link or No Search Criteria')

        return searchList

