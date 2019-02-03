import webbrowser
import time
import scraper as s

def main():
    # Search test
    start = time.time()
    search = s.Search()
    search.setInitTitleSearchURL()
    search.insertURLAddon("TITLE_TYPE", "feature")
    search.insertURLAddon("TITLE_SEARCH", "Empire")
    searches = search.getSearches()
    print(searches)
    end = time.time()
    print(end - start)

    # PageInfo test
    start = time.time()
    info = s.PageInfo('https://www.imdb.com/title/tt7286456/').getPageInfo()
    print(list(info['CAST'].keys()))

    end = time.time()

    print(end-start)

if __name__ == '__main__':
    main()