from requests import get
from requests.exceptions import RequestException
from bs4 import BeautifulSoup as bs
from contextlib import closing
import re
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
                html = response.content
                return html

    except RequestException as e:
        print(str(e))
        return str()


def checkResponse(response):
    goodResponse = False
    print(response.status_code)
    if response.status_code == 200:
        goodResponse = True

    return goodResponse

class PageInfo:
    def __init__(self, url):
        self.url = url
        self.urlContent = get_url_content(self.url)

    def getPageInfo(self):
        pageInfo = dict()

        if URL_ADDON['NAME'] in self.url:
            pageInfo = self.getNamePageInfo()

        elif URL_ADDON['TITLE'] in self.url:
            pageInfo = self.getTitlePageInfo()

        return pageInfo

    def getRuntime(self, runtime=str()):
        timelist = runtime.split(' ')

        return (int(timelist[0].replace('h', '')) * 60) + (int(timelist[1].replace('min', '')))

    def getTitlePageInfo(self):
        pageInfo = {'TITLE': str(),
                    'YEAR': int(),
                    'GENRES': list(),
                    'RUNTIME': int(),
                    'RATING': str(),
                    'POSTER': str(),
                    'CAST': dict(),
                    'DIRECTOR': list(),
                    'WRITERS': list()
                    }

        html = bs(self.urlContent, 'html.parser')

        # get everything in title bar
        titleBar = html.find('div', class_='titleBar')
        subText = titleBar.find('div', class_='subtext')
        plot_summary = html.find('div', class_='plot_summary')

        # get the cast list
        castList = html.find('table', class_='cast_list')

        # POSTER:
        poster = html.find('div', class_='poster')

        # TITLE:
        title = titleBar.find('div', class_='title_wrapper').h1

        # YEAR:
        year = title.span
        year.extract()

        # RATING:
        rating = subText

        # RUNTIME:
        runtime = rating.time
        runtime.extract()

        # GENRES:
        genres = rating.findAll('a')

        for genre in genres:
            pageInfo['GENRES'].append(str(genre.text).lower())
            genre.extract()

        # remove the release date from the GENRES list
        pageInfo['GENRES'].pop()

        # DIRECTOR and WRITERS:
        summaryItems = plot_summary.find_all('div', class_='credit_summary_item')

        for item in summaryItems:
            if any(word in str(item.h4.text) for word in ['Writers:', 'Writer:', 'Directors:', 'Director:']):
                names = item.findAll('a')

                for name in names:
                    if 'more credit' not in str(name.text):
                        if any(word in str(item.h4.text) for word in ['Writers:', 'Writer:']):
                            pageInfo['WRITERS'].append(str(name.text))
                        else:
                            pageInfo['DIRECTOR'].append(str(name.text))

        # CAST:
        castItems = castList.find_all('tr')

        for item in range(len(castItems)):
            if item > 0:
                castMember = dict()

                # ACTOR NAME
                actorName = castItems[item]
                actorName.td.extract()

                castMember['ACTOR_LINK'] = DEFAULT_PATH + str(actorName.td.a['href']).lstrip().rstrip()

                # CHARACTER NAME
                castMember['CHARACTER'] = re.sub(' +', ' ', str(actorName.find('td', class_='character').text).lstrip().rstrip().replace('\n', ''))

                pageInfo['CAST'][str(actorName.td.a.text).lstrip().rstrip()] = castMember

        # Add rest of values to their respective key
        pageInfo['TITLE'] = str(title.text).replace('\xa0', '').rstrip()
        pageInfo['YEAR'] = int(str(year.a.text))
        pageInfo['RUNTIME'] = self.getRuntime(str(runtime.text).lstrip())
        pageInfo['RATING'] = str(rating.text).lstrip().replace('|', '').replace(',', '').rstrip()
        pageInfo['POSTER'] = str(poster.a.img['src'])

        return pageInfo

    def checkIfMovie(self, title):
        isMovie = True
        bannedKeywords = ['short',
                          'Short',
                          'Video Game',
                          'TV'
                          ]
        if any(s in str(title.text) for s in bannedKeywords):
            isMovie = False
        if len(title.find_all('div', class_='filmo-episodes')) > 0:
            isMovie = False
        if len(title.find_all('a', class_='in_production')) > 0:
            isMovie = False

        return isMovie

    def getNamePageInfo(self):
        pageInfo = {'NAME': str(),
                    'IMAGE': str(),
                    'DOB': str(),
                    'ACTOR_LIST': list(),
                    'WRITER_LIST': list(),
                    'DIRECTOR_LIST': list(),
                    'PRODUCER_LIST': list()
                    }

        html = bs(self.urlContent, 'html.parser')

        # Get basic actor info:
        actorInfo = html.find('div', class_='article name-overview')
        actorHeaderInfo = actorInfo.find('td', {'id': 'overview-top'})
        imgInfo = actorInfo.find('td', {'id': 'img_primary'})
        filmography = html.find('div', {'id': 'filmography'}).find_all('div', class_='filmo-category-section')

        # NAME:
        pageInfo['NAME'] = str(actorHeaderInfo.h1.span.text)

        # DOB:
        dob = actorHeaderInfo.find('div', {'id': 'name-born-info'})

        if str(dob) != 'None':
            pageInfo['DOB'] = str(dob.time['datetime'])
        else:
            pageInfo['DOB'] = str()

        # IMAGE:
        image = imgInfo.div.a

        if str(image) != 'None':
            pageInfo['IMAGE'] = str(image.img['src'])
        else:
            pageInfo['IMAGE'] = str()

        # Filmography (ACTOR_LIST, WRITER_LIST, DIRECTOR_LIST, PRODUCER-LIST):

        for section in filmography:
            titles = section.findAll('div', id=re.compile('^director-|^actor-|^writer-|^producer-|^actress-'))

            if len(titles) > 0:
                for title in titles:
                    titleInfo = list()

                    if self.checkIfMovie(title):
                        # Get Movie Title:
                        film = str(title.b.a.text)
                        titleInfo.append(film)

                        # Get Movie Year:

                        year = re.findall('\d+', str(title.find('span', class_='year_column').text))
                        titleInfo.append(int(year[0]))

                        # Get IMDB link:
                        link = DEFAULT_PATH + str(title.b.a['href'])
                        titleInfo.append(link)

                        if any(atype in title['id'] for atype in ['actress-', 'actor-']):
                            pageInfo['ACTOR_LIST'].append(titleInfo)
                        elif 'writer-' in title['id']:
                            pageInfo['WRITER_LIST'].append(titleInfo)
                        elif 'director-' in title['id']:
                            pageInfo['DIRECTOR_LIST'].append(titleInfo)
                        elif 'producer-' in title['id']:
                            pageInfo['PRODUCER_LIST'].append(titleInfo)

        return pageInfo

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
            rawList = html.find_all('div', class_='lister-item mode-advanced', limit=10)

            if self.getInitNameSearchURL() in self.getSearchURL():
                rawList = html.find_all('div', class_='lister-item mode-detail', limit=10)

            # To minimize time spent parsing info, number of list items will be reduced to 10

            for listItem in rawList:
                searchInfo = list()

                name = str(listItem.h3.a.text).lstrip().replace("\n", '')
                searchInfo.append(name)

                if self.getInitTitleSearchURL() in self.getSearchURL():
                    year = str(listItem.find('span', class_='lister-item-year text-muted unbold').text)
                    searchInfo.append(int(str(year).replace('(', '').replace(')', '')))

                searchInfo.append(str(DEFAULT_PATH + listItem.a['href']))
                searchList.append(searchInfo)

        else:
            print('Bad Link or No Search Criteria')

        return searchList
