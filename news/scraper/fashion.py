from bs4 import BeautifulSoup
import requests




class Scraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
        }




class GlamourScraper(Scraper):
    def __init__(self, topic):
        self.url = 'https://www.glamourmagazine.co.uk/topic/'+topic
        Scraper.__init__(self)

    def scrape(self):
        articles = []
        request = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(request.text, 'html.parser')
        #print(soup)
        for article in soup.select('div[class*="SummaryItemWrapper"]'):
            article_title = article.text
            article_image = article.find('img')['src']
            article_url = article.find('a')['href']
            articles.append(
                    {'title': article_title, 'url': self.url+article_url, 'img': article_image})
        
        return articles

class PeopleScraper(Scraper):
    def __init__(self, topic):
        self.url = 'https://people.com/'+topic+'/'
        Scraper.__init__(self)

    def scrape(self):
        articles = []
        request = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(request.text, 'html.parser')
        #print(soup)
        for article in soup.select('div[class*="category-page-item"]'):
            try:
                article_title = article.find('span').text.strip()
                
                article_image = article.find('img')['src']
                article_url = article.find('a')['href']
                articles.append(
                        {'title': article_title, 'url': self.url+article_url, 'img': article_image})
            except :
                pass
        
        return articles