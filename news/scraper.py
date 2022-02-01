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


class GoalDotComScraper(Scraper):
    def __init__(self) -> None:
        self.url = 'https://www.goal.com'

    def scrape(self):

        request = requests.get(self.url + '/en-ng/news/1')
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
                print(e)

        return headlines


class SkySportScraper(Scraper):
    def __init__(self) -> None:
        self.url = 'https://www.skysports.com/news-wire'

        Scraper.__init__(self)

    def scrape(self):

        request = requests.get(self.url, headers=self.headers)
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
        self.url = 'https://www.premierleague.com'

        Scraper.__init__(self)

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
        self.url = 'https://www.laliga.com'

    def scrape(self):

        request = requests.get(self.url + '/en-ES/news', verify=False)
        soup = BeautifulSoup(request.text, 'html.parser')
        news = soup.find_all(
            'div', {'class': 'styled__ImageContainer-sc-1si1tif-0'})

        articles = []

        try:
            for article in news:
                title = article.find('h3').text
                url = self.url + article.find('a')['href']
                img = 'https://assets.laliga.com/assets/2019/10/09/medium/47d73a0eff4508d03ea51f26384bcba2.jpeg'
                articles.append({'title': title, 'url': url, 'img': img})
        except Exception as e:
            print(e)
            pass

        return articles


class BundesligaScraper(Scraper):
    def __init__(self) -> None:
        self.url = 'https://www.bundesliga.com'

        Scraper.__init__(self)

    def scrape(self):
        articles = []
        request = requests.get(
            self.url + '/en/bundesliga', headers=self.headers)
        soup = BeautifulSoup(request.text, 'html.parser')
        news = soup.select('.teaser')
        other_news = soup.select('.topListEntry')

        for article in news:
            article_title = article.find('h2').text
            article_url = self.url + article.find('a')['href']
            article_image = article.find('img')['src'].split('?')[0]

            articles.append(
                {'title': article_title.strip(), 'url': article_url, 'img': article_image})

        for article in other_news:
            article_title = article.text
            article_url = self.url + article['href']
            article_image = article.find('img')['src'].split('?')[0]

            articles.append(
                {'title': article_title.strip(), 'url': article_url, 'img': article_image})

        return articles


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

    categories = ['', 'plugged', 'neural', 'shift',
                  'growth-quarters', 'hardfork', 'house-of-talent']

    def __init__(self, category='') -> None:
        self.category = category
        self.url = 'https://thenextweb.com/'

    def scrape(self):

        articles = []
        request = requests.get(self.url + self.category)
        soup = BeautifulSoup(request.text, 'html.parser')

        if self.category == '':
            news = soup.select('.c-showcase__grid article')
            for article in news:
                article_title = article.select_one(
                    '.c-card__heading').text.strip()
                article_url = article.select_one('a')['href']
                article_image = article.select_one('img')['src']

                articles.append({'title': article_title.strip(),
                                'url': article_url, 'img': article_image})


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
NewsBlockScraper().scrape()