import webbrowser
from scraper import Search

def main():
    search = Search()
    search.setInitTitleSearchURL()
    search.insertURLAddon("TITLE_TYPE", "feature")
    search.insertURLAddon("TITLE_SEARCH", "empire")
    print(search.getSearchURL())
    print(search.getSearches())

if __name__ == '__main__':
    main()