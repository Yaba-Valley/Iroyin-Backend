from bs4 import BeautifulSoup
from .base import Scraper


class GlamourScraper(Scraper):
    def __init__(self, topic='entertainment'):
        self.url = 'https://www.glamourmagazine.co.uk'
        self.title = 'Glamour'
        self.topic = topic
        self.favicon = 'https://www.glamourmagazine.co.uk/verso/static/glamour-international/assets/favicon.ico'

        Scraper.__init__(self, 'Glamour Scraper')

    async def scrape(self, async_client, scraped_news):
        async with async_client.get(self.url+'/topic/'+self.topic, headers=self.headers) as response:
            articles = []
            request_text = await response.text()
            soup = BeautifulSoup(request_text, 'html.parser')

            for article in soup.select('div[class*="SummaryItemWrapper"]'):
                article_title = article.text
                article_image = article.find('img')['src']
                article_url = article.find('a')['href']
                articles.append(
                    {'title': article_title, 'url': self.url+article_url, 'img': article_image, 'metadata': {'website': self.title, 'favicon': self.favicon}})

            scraped_news.extend(articles)
            return articles


class PeopleScraper(Scraper):
    def __init__(self, topic=False):

        if topic:
            self.url = f"https://people.com/{topic}"
        else:
            self.url = 'https://people.com/tag/news'

        self.title = "People.com"
        self.favicon = 'https://people.com/img/favicons/favicon-152.png'

        Scraper.__init__(self, 'People Scraper')

    async def scrape(self, async_client, scraped_news):
        async with async_client.get(self.url, headers=self.headers) as response:
            articles = []
            response_text = await response.text()
            soup = BeautifulSoup(response_text, 'html.parser')

            for article in soup.find_all("a", class_="mntl-document-card"):
                try:
                    article_title = article.find(
                        'span', class_='card__title-text').text
                    article_image = article.find('img').get('src')
                    article_url = article['href']

                    articles.append(
                        {'title': article_title, 'url': article_url, 'img': article_image, 'metadata': {'website': self.title, 'favicon': self.favicon}})
                except Exception as e:
                    print(e)

            scraped_news.extend(articles)
            return scraped_news
