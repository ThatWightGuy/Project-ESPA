import imdbscraper as iws
import mysql.connector
import re

class ConvertScrape:
    def __init__(self, url):
        self.url = url
        self.pageInfo = self.scrapePageInfo()

    def scrapePageInfo(self):
        pageInfo = iws.PageInfo(self.url)

        return pageInfo.getPageInfo()

    def convertInfo(self):
        if iws.URL_ADDON['TITLE'] in self.url:
            self.convertTitleInfo()

        elif iws.URL_ADDON['NAME'] in self.url:
            self.convertNameInfo()

    def getIDFromURL(self):
        return re.findall('(\d{7})', self.url)

    def convertTitleInfo(self):
        movieId = self.getIDFromURL()[0]

        # TODO: create specific job IDs from scrape info

        return None

    def convertNameInfo(self):
        personID = self.getIDFromURL()[0]

        # TODO: create specific job IDs from scrape info

        return None