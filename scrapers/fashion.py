from bs4 import BeautifulSoup
from .base import Scraper
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md


class GlamourScraper(Scraper):
    def __init__(self, topic='entertainment'):
        self.url = 'https://www.glamourmagazine.co.uk'
        self.title = 'Glamour'
        self.topic = topic
        """ 
        topic can be either of the following:
        makeup, hair, skin, fashion, empowerment, entertainment, wellness, 
        """
        self.favicon = 'https://www.glamourmagazine.co.uk/verso/static/glamour-international/assets/favicon.ico'

        Scraper.__init__(self, 'Glamour Scraper')

    async def scrape(self, async_client, scraped_news, failed_scrapers):
        try:
            print(f'scraping {self.url}/topic/{self.topic}')
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
        except Exception as e:
            print(f'{self.url}/topic/{self.topic}')
            failed_scrapers.append({'url': self.url, 'error': str(e)})
            pass

    def scrape_news_content(self, url):
        res_text = requests.get(url).text
        soup = BeautifulSoup(res_text, 'html.parser')

        scripts = soup.find_all('script')

        for script in scripts:
            script.decompose()

        text_content = soup.find('div', class_='body__inner-container')

        return md(str(text_content))


class PeopleScraper(Scraper):
    def __init__(self, topic=''):

        if topic:
            self.url = f"https://people.com/{topic}"
        else:
            self.url = 'https://people.com/tag/news'

        self.title = "People.com"
        self.favicon = 'https://people.com/img/favicons/favicon-152.png'

        Scraper.__init__(self, 'People Scraper')

    async def scrape(self, async_client, scraped_news, failed_scrapers):

        try:
            print('scraping', self.url)
            async with async_client.get(self.url, headers=self.headers) as response:
                articles = []
                response_text = await response.text()
                soup = BeautifulSoup(response_text, 'html.parser')

                for article in soup.find_all("a", class_="mntl-document-card"):
                    try:
                        article_title = article.find(
                            'span', class_='card__title-text').text
                        article_image = article.find('img')['data-src']
                        article_url = article['href']

                        articles.append(
                            {'title': article_title, 'url': article_url, 'img': article_image, 'metadata': {'website': self.title, 'favicon': self.favicon}})
                    except Exception as e:
                        print(e)

                scraped_news.extend(articles)
                return scraped_news
        except Exception as e:
            print(self.url, 'is not working')
            failed_scrapers.append({'url': self.url, 'error': str(e)})
            pass

    def scrape_news_content(self, url):
        res_text = requests.get(url).text
        soup = BeautifulSoup(res_text, 'html.parser')

        scripts = soup.find_all('script')

        for script in scripts:
            script.decompose()

        text_content = soup.find('div', class_='article-content')

        return md(str(text_content))
