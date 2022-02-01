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
        
    def scrape(self):
        request = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(request.text, 'html.parser')
        
        articles = []
        
        for article in soup.select('.mntl-document-card'):
            article_title = article.select_one('.card__title-text').text
            article_image = article.select_one('img')['src']
            article_url = article['href']
            
            articles.append({'title': article_title, 'img': article_image, 'url': article_url})
            
        return articles
    
#print(VeryWellMindScraper().scrape())