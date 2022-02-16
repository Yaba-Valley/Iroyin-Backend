import requests
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
        }


class VeryWellMindScraper(Scraper):
    def __init__(self) -> None:
        self.url = 'https://www.verywellmind.com/news-latest-research-and-trending-topics-4846421'
        Scraper.__init__(self)
        
    async def scrape(self, async_client, scraped_news):
        async with async_client.get(self.url, headers=self.headers) as response:
            request_text = await response.text()
            soup = BeautifulSoup(request_text, 'html.parser')
            
            articles = []
            
            for article in soup.select('.mntl-document-card'):
                print(article)
                article_title = article.select_one('.card__title-text').text
                article_image = article.select_one('.card__media img')['data-src']
                article_url = article['href']
                print(articles)
                
                articles.append({'title': article_title, 'img': article_image, 'url': article_url})
              
            scraped_news.extend(articles)
            return articles
    
#print(VeryWellMindScraper().scrape())