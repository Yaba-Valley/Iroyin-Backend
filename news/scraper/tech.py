import requests
from bs4 import BeautifulSoup
from .base import Scraper


class FreeCodeCampScraper(Scraper):

    def __init__(self) -> None:
        self.url = 'https://www.freecodecamp.org'

        Scraper.__init__(self)

    def scrape(self):
        request = requests.get(self.url + '/news', headers=self.headers)
        soup = BeautifulSoup(request.text, 'html.parser')
        news = soup.find_all('article', {'class': 'post-card'})

        articles = []

        for article in news:
            article_title = article.find(
                'h2', {'class': 'post-card-title'}).text
            article_image = article.select_one(
                '.post-card-image-link img')['src']
            article_url = article.find(
                'h2', {'class': 'post-card-title'}).find('a')['href']

            articles.append({'title': article_title.strip(), 'url': self.url +
                            article_url, 'img': article_image})

        return articles


class TechCrunchScraper(Scraper):
    def __init__(self):
        self.url = 'https://techcrunch.com'

        Scraper.__init__(self)

    def scrape(self):
        request = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(request.text, 'html.parser')

        news = soup.find_all('article')

        articles = []

        for article in news:
            print(article)
            article_title = article.find(
                'a', {'class': 'post-block__title__link'}).text
            article_url = article.find(
                'a', {'class': 'post-block__title__link'})['href']
            article_image = article.find('img')['src']

            articles.append(
                {'title': article_title.strip(), 'url': article_url, 'img': article_image})

        return articles


class TechTrendsAfricaScraper(Scraper):
    def __init__(self):
        self.url = 'https://techtrends.africa'
        Scraper.__init__(self)

    def scrape(self):
        request = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(request.text, 'html.parser')

        news = soup.find_all('article')

        articles = []

        for article in news:
            article_title = article.select_one('.jeg_post_title').text
            article_url = article.select_one(
                '.jeg_post_title').find('a')['href']

            if article.find('img') == None:
                article_image = article.find(
                    'div', {'class': 'thumbnail-container thumbnail-background'})['data-src']
            else:
                article_image = article.find('img')['data-src']

            articles.append(
                {'title': article_title.strip(), 'url': article_url, 'img': article_image.split('?')[0]})

        return articles


class GizModoScraper:
    def __init__(self):
        self.url = 'https://gizmodo.com/'

    def scrape(self):
        request = requests.get(self.url)
        soup = BeautifulSoup(request.text, 'html.parser')

        news = soup.find_all('article')

        articles = []

        for article in news:
            try:
                article_title = article.select_one('h4').text
                article_url = article.select_one('a')['href']
                article_image = article.select_one('img')['src']

                articles.append({'title': article_title.strip(),
                                'img': article_image, 'url': article_url})

            except:
                continue

        return articles


class TheNextWebScraper:

    categories = ['latest', 'plugged', 'neural', 'shift',
                  'growth-quarters', 'hardfork', 'house-of-talent', 
                  'future-of-finance', 'readme'
                ]

    def __init__(self, category=categories[6]) -> None:
        self.category = category
        self.url = 'https://thenextweb.com/'

    def scrape(self):

        articles = []
        request = requests.get(self.url + self.category)
        soup = BeautifulSoup(request.text, 'html.parser')

        news = soup.select('article')

        for article in news:
            if article.select_one('.c-card__heading') == None:
                article_title = article.select_one('h4').text.strip()
                article_url = self.url + article.select_one('a')['href'][1:]
                article_image = article.select_one('img')['data-src']

                articles.append({'title': article_title.strip(),
                                'url': article_url, 'img': article_image})
            else:
                article_title = article.select_one('h3').text.strip()
                article_url = self.url + article.select_one('a')['href']
                article_image = article.select_one('img')['data-src']

                articles.append(
                    {'title': article_title, 'url': article_url, 'img': article_image})

        return articles


class GlassDoorScraper:
    def __init__(self) -> None:
        self.url = 'https://glassdoor.com'

    def scrape(self):
        articles = []

        request = requests.get(self.url + '/blog')
        soup = BeautifulSoup(request.text, 'html.parser')

        for article in soup.select('.post'):
            article_title = article.select_one('h3').text
            article_url = self.url + article.select_one('a')['href']
            article_image = article.select_one(
                '.css-6uzs0z')['style'].split('url(')[1].split(')')[0]

            articles.append(
                {'title': article_title, 'img': article_image, 'url': article_url})

        for article in soup.select('.featured-article'):
            article_title = article.select_one('h2').text
            article_url = article.select_one('a')['href']
            article_image = article.select_one('img')['src']

            print(article_title, article_url, article_image)
            articles.append(
                {'title': article_title, 'img': article_image, 'url': article_url})

        print(len(articles))
        return articles

class NewsBlockScraper(Scraper):
    def __init__(self):
        self.url = 'https://newblock.news/'
        Scraper.__init__(self)

    def scrape(self):
        request = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(request.text, 'html.parser')

        news = soup.find_all('article')

        articles = []

        for article in news:
            try:
                article_title = article.find('h3').text
                article_image = article.find('img')['data-src']
                article_url = article.find('a')['href']
                print(article_title)
                print('\n')
                articles.append(
                    {'title': article_title, 'url': article_url, 'img': article_image})
            except:
                pass
        return articles

#print(GlassDoorScraper().scrape())
