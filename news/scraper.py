from bs4 import BeautifulSoup
import requests
#import cfscrape

from .scraper.base import Scraper

class PunchScraper(Scraper):
    def __init__(self, topic) -> None:
        self.url = f'https://punchng.com/topics/{topic}/'

        Scraper.__init__(self)

    def scrape(self):

        request = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(request.text, 'html.parser')

        value = soup.find_all('article', {'class': 'entry-item-simple'})
        headlines = []

        for i in value:
            try:
                img = i.find('img').get('src')
                news = i.find('h3', {'class': 'entry-title'}).text
                link = i.find('h3', {'class': 'entry-title'}).find('a')['href']
                headlines.append({'title': news, 'url': link, 'img': img})
            except:
                pass

        return headlines


class VanguardScraper(Scraper):
    def __init__(self, topic) -> None:
        self.url = f'https://www.vanguardngr.com/category/{topic}/'

        Scraper.__init__(self)

    def scrape(self):

        # get big thumbnail news
        request = requests.get(self.url, headers=self.headers).content
        soup = BeautifulSoup(request, 'lxml')
        value = soup.find_all('h2', {'class': 'entry-title'})

        headlines = [
            {'title': i.text, 'url': i.find('a')['href']} for i in value]

        return headlines
