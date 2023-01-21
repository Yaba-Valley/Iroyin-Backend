from bs4 import BeautifulSoup
from .base import Scraper


class VeryWellMindScraper(Scraper):
    def __init__(self) -> None:
        self.url = 'https://www.verywellmind.com/news-latest-research-and-trending-topics-4846421'
        self.title = 'VeryWellMind'
        self.favicon = 'https://www.verywellmind.com/favicon.ico'

        Scraper.__init__(self, 'VeryWellMind Scraper')

    async def scrape(self, async_client, scraped_news):
        async with async_client.get(self.url, headers=self.headers) as response:
            request_text = await response.text()
            soup = BeautifulSoup(request_text, 'html.parser')

            articles = []

            for article in soup.select('.mntl-document-card'):

                article_title = article.select_one('.card__title-text').text
                image = article.find('img');
                article_image = ''
                
                if image:
                    article_image = image.attrs['data-src']
                    
                article_url = article['href']

                articles.append({'title': article_title, 'img': article_image, 'url': article_url, 'metadata': {
                                'website': self.title, 'favicon': self.favicon}})

            scraped_news.extend(articles)
            return articles

# print(VeryWellMindScraper().scrape())
