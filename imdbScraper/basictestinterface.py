import webbrowser
import time
import scraper as s

def main():

    # Search test
    start = time.time()
    s.get_url_content("https://www.twitter.com")
    end = time.time()
    print(end - start)

    start = time.time()
    search = s.Search()
    search.setInitTitleSearchURL()
    search.insertURLAddon("TITLE_TYPE", "feature")
    search.insertURLAddon("TITLE_SEARCH", "Baby Driver")
    searches = search.getSearches()
    print(searches)

    # PageInfo test
    info = s.PageInfo(searches[0][2])
    print(info.getPageInfo())

    end = time.time()

    print(end-start)

if __name__ == '__main__':
    main()