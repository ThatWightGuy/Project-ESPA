import webbrowser
import time
import imdbscraper as iws
import re
import ScrapeToDatabase as std

def main():
    # Search test
    '''start = time.time()
    search = iws.Search()
    search.setInitTitleSearchURL()
    search.insertURLAddon("TITLE_TYPE", "feature")
    search.insertURLAddon("TITLE_SEARCH", "Empire")
    searches = search.getSearches()
    print(searches)
    end = time.time()
    print(end - start)

    # PageInfo test
    start = time.time()
    info = iws.PageInfo('https://www.imdb.com/title/tt7286456/').getPageInfo()
    print(info)

    end = time.time()

    print(end-start)'''

    print(re.findall('(tt|nm)(\d{7})', 'https://www.imdb.com/title/tt7286456/'))

if __name__ == '__main__':
    main()