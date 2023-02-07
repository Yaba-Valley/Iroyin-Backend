from bs4 import BeautifulSoup
import requests
from markdownify import markdownify as md
from .base import Scraper


class VeryWellMindScraper(Scraper):
    def __init__(self) -> None:
        self.url = 'https://www.verywellmind.com/news-latest-research-and-trending-topics-4846421'
        self.title = 'VeryWellMind'
        self.favicon = 'https://www.verywellmind.com/favicon.ico'

        Scraper.__init__(self, 'VeryWellMind Scraper')

    async def scrape(self, async_client, scraped_news, failed_scrapers):
        try:
            print(f'scraping {self.url}')
            async with async_client.get(self.url, headers=self.headers) as response:
                request_text = await response.text()
                soup = BeautifulSoup(request_text, 'html.parser')

                articles = []

                for article in soup.select('.mntl-document-card'):

                    article_title = article.select_one(
                        '.card__title-text').text
                    image = article.find('img')
                    article_image = ''

                    if image:
                        article_image = image.attrs['data-src']

                    article_url = article['href']

                    articles.append({'title': article_title, 'img': article_image, 'url': article_url, 'metadata': {
                                    'website': self.title, 'favicon': self.favicon}})

                scraped_news.extend(articles)
                return articles
        except Exception as e:
            print(self.url, 'is not working')
            failed_scrapers.append({ 'url': self.url, 'error': str(e) })
            pass

    def scrape_news_content(self, url):
        res_text = requests.get(url).text
        soup = BeautifulSoup(res_text, 'html.parser')

        article_content = soup.find(
            'div', class_='comp structured-content article-content expert-content right-rail__offset lock-journey health-sc-page mntl-sc-page mntl-block')

        print(article_content)

        return md(str(article_content))
