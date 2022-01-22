from cmath import e
from bs4 import BeautifulSoup
import requests
#import cfscrape


class Scraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
        }


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

# FIXME: THE CFSCRAPE ERROR


class VanguardScraper(Scraper):
    def __init__(self, topic) -> None:
        self.url = f'https://www.vanguardngr.com/category/{topic}/'

    def scrape(self):

        # get big thumbnail news
        request = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(request, 'html.parser')
        value = soup.find_all('h2', {'class': 'entry-title'})

        print(soup)

        headlines = [
            {'title': i.text, 'url': i.find('a')['href']} for i in value]

        return headlines


class GoalDotComScraper(Scraper):
    def __init__(self) -> None:
        self.url = 'https://www.goal.com/en-ng/news/1'

    def scrape(self):

        request = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(request.text, 'html.parser')
        value = soup.find_all('tr')
        headlines = []

        for i in value:
            try:
                img = i.find('img').get('src')
                news = i.find(
                    'h3', {'class': 'widget-news-card__title'})['title']
                link = self.url+i.find('a')['href']
                headlines.append({'title': news, 'url': link, 'img': img})
            except Exception as e:
                pass

        return headlines


class SkySportScraper(Scraper):
    def __init__(self) -> None:
        self.url = 'https://www.skysports.com/news-wire'

    def scrape(self):

        request = requests.get(self.url, headers = self.headers)
        soup = BeautifulSoup(request.text, 'html.parser')
        news = soup.find_all(
            'div', {'class': 'news-list__item news-list__item--show-thumb-bp30'})
        #news = soup.find_all('a', {'class': 'news-list__headline-link'})
        # print(news)

        headlines = [{'title': article.find('a', {'class': 'news-list__headline-link'}).text.strip(), 'url': article.find('a', {'class': 'news-list__headline-link'})['href'], 'img':article.find('img')['data-src']}
                     for article in news]

        return headlines


class EPLScraper(Scraper):
    def __init__(self) -> None:
        # the breaking news section of goal dot com (nigeria version)
        self.url = 'https://www.premierleague.com'

    def scrape(self):

        request = requests.get(self.url+'/news', headers=self.headers)
        soup = BeautifulSoup(request.text, 'html.parser')
        news = soup.find_all('a', {'class': 'thumbnail thumbLong'})

        headlines = [{'title': article.find('span', {'class': 'title'}).text, 'url': self.url +
                      article['href'], 'img':article.find('img')['src'].strip()} for article in news]

        return headlines


class LaLigaScraper(Scraper):
    def __init__(self) -> None:
        # images of laliga cannot be scraped cause of it JS abi CSS sha
        self.url = 'https://www.laliga.com/en-ES/news'

    def scrape(self):

        request = requests.get(self.url, verify=False, headers= self.headers)
        soup = BeautifulSoup(request.text, 'html.parser')
        news = soup.find_all(
            'div', {'class': 'styled__LastNewContainer-ddibnj-4 buiYod'})
        print(news[0])

        headlines = []
        try:
            for article in news:
                title = article.find(
                    'h3', {'class': 'styled__TextHeaderStyled-sc-1edycnf-0'}).text
                url = article.find('a')['href']
                img = article.find('img')['src'].strip()
                headlines.append({'title': title, 'url': url, 'img': img})
        except:
            pass

        return headlines


class BundesligaScraper(Scraper):
    def __init__(self) -> None:
        self.url = 'https://www.bundesliga.com/en/bundesliga'

    def scrape(self):
        request = requests.get(self.url, headers = self.headers)
        return []


class FreeCodeCampScraper(Scraper):

    def __init__(self) -> None:
        self.url = 'https://www.freecodecamp.org'

    def scrape(self):
        request = requests.get(self.url + '/news', headers = self.headers)
        soup = BeautifulSoup(request.text, 'html.parser')
        news = soup.find_all('article', {'class': 'post-card'})

        articles = []

        for article in news:
            article_title = article.find(
                'h2', {'class': 'post-card-title'}).text
            article_image = article.find(
                'img', {'class': 'post-card-image'})['data-src']
            article_url = article.find(
                'h2', {'class': 'post-card-title'}).find('a')['href']

            articles.append({'title': article_title, 'url': self.url +
                            article_url, 'img': self.url + article_image})

        return articles


class TechCrunchScraper(Scraper):
    def __init__(self):
        self.url = 'https://techcrunch.com'

    def scrape(self):
        request = requests.get(self.url, headers = self.headers)
        soup = BeautifulSoup(request.text, 'html.parser')

        news = soup.find_all('article', {'class': 'post-block'})

        articles = []

        print(news)

        for article in news:
            article_title = article.find(
                'a', {'class': 'post-block__title__link'}).text
            article_url = article.find(
                'a', {'class': 'post-block__title__link'})['href']
            article_image = article.find('img')['src']

            articles.append(
                {'title': article_title, 'url': article_url, 'img': article_image})

        return articles


class TechTrendsAfricaScraper(Scraper):
    def __init__(self):
        self.url = 'https://techtrends.africa'
        Scraper.__init__(self)

    def scrape(self):
        request = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(request.text, 'html.parser')

        print(soup)

        news = soup.find_all('article')

        articles = []

        for article in news:
            article_title = article.find(
                'h2', {'class': 'jeg_post_title'}).text
            article_url = article.find(
                'h2', {'class': 'jeg_post_title'}).find('a')['href']
            article_image = article.find(
                'div', {'class': 'thumbnail-container thumbnail-background'}['data-src'])

            articles.append(
                {'title': article_title, 'url': article_url, 'img': article_image})

        return articles


