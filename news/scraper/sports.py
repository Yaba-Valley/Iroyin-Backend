from urllib import response
import requests
from bs4 import BeautifulSoup
from .base import Scraper


class VanguardScraper(Scraper):
    def __init__(self, topic='sports') -> None:
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


class PunchScraper(Scraper):
    def __init__(self, topic='sports') -> None:
        self.url = f'https://punchng.com/topics/{topic}/'

        Scraper.__init__(self)

    async def scrape(self, async_client, scraped_news):

        async with async_client.get(self.url, headers=self.headers) as response:
            html_text = await response.text()

            soup = BeautifulSoup(html_text, 'html.parser')

            value = soup.find_all('article', {'class': 'entry-item-simple'})
            headlines = []

            for i in value:
                try:
                    img = i.find('img').get('src')
                    news = i.find('h3', {'class': 'entry-title'}).text
                    link = i.find(
                        'h3', {'class': 'entry-title'}).find('a')['href']
                    headlines.append({'title': news, 'url': link, 'img': img})
                except:
                    pass

            scraped_news.extend(headlines)
            return headlines



class GoalDotComScraper(Scraper):
    def __init__(self) -> None:
        self.url = 'https://www.goal.com'

    async def scrape(self, async_client, scraped_news):

        async with async_client.get(self.url + '/en-ng/news/1') as response:
            html_text = await response.text()
            soup = BeautifulSoup(html_text, 'html.parser')
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

            scraped_news.extend(headlines)
            return headlines


class SkySportScraper(Scraper):
    def __init__(self) -> None:
        self.url = 'https://www.skysports.com/news-wire'

        Scraper.__init__(self)

    async def scrape(self, async_client, scraped_news):

        async with async_client.get(self.url, headers=self.headers) as response:
            html_text = await response.text()
            soup = BeautifulSoup(html_text, 'html.parser')
            news = soup.find_all(
                'div', {'class': 'news-list__item news-list__item--show-thumb-bp30'})

            headlines = [{'title': article.find('a', {'class': 'news-list__headline-link'}).text.strip(), 'url': article.find('a', {'class': 'news-list__headline-link'})['href'], 'img':article.find('img')['data-src']}
                         for article in news]

            scraped_news.extend(headlines)
            return headlines


class EPLScraper(Scraper):
    def __init__(self) -> None:
        self.url = 'https://www.premierleague.com'

        Scraper.__init__(self)

    async def scrape(self, async_client, scraped_news):

        async with async_client.get(self.url+'/news', headers=self.headers) as response:
            html_text = await response.text()
            soup = BeautifulSoup(html_text, 'html.parser')
            news = soup.find_all('a', {'class': 'thumbnail thumbLong'})

            headlines = [{'title': article.find('span', {'class': 'title'}).text, 'url': self.url +
                          article['href'], 'img':article.find('img')['src'].strip()} for article in news]

            scraped_news.extend(headlines)
            return headlines


class LaLigaScraper(Scraper):
    def __init__(self) -> None:
        # images of laliga cannot be scraped cause of it JS abi CSS sha
        self.url = 'https://www.laliga.com'

    async def scrape(self, async_client, scraped_news):

        async with async_client.get(self.url + '/en-ES/news') as response:
            html_text = await response.text()
            soup = BeautifulSoup(html_text, 'html.parser')
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

            scraped_news.extend(articles)
            return articles


class BundesligaScraper(Scraper):
    def __init__(self) -> None:
        self.url = 'https://www.bundesliga.com'

        Scraper.__init__(self)

    async def scrape(self, async_client, scraped_news):
        
        async with async_client.get(self.url + '/en/bundesliga', headers=self.headers) as response:

            articles = []
            html_text = await response.text()
            soup = BeautifulSoup(html_text, 'html.parser')
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

            scraped_news.extend(articles)
            return articles
