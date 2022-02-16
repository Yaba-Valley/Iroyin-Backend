from bs4 import BeautifulSoup




class Scraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
        }




class GlamourScraper(Scraper):
    def __init__(self, topic = 'entertainment'):
        self.url = 'https://www.glamourmagazine.co.uk/topic/'+topic
        Scraper.__init__(self)

    async def scrape(self, async_client, scraped_news):
        async with async_client.get(self.url, headers=self.headers) as response:
            articles = []
            request_text = await response.text()
            soup = BeautifulSoup(request_text, 'html.parser')
            #print(soup)
            for article in soup.select('div[class*="SummaryItemWrapper"]'):
                article_title = article.text
                article_image = article.find('img')['src']
                article_url = article.find('a')['href']
                articles.append(
                        {'title': article_title, 'url': self.url+article_url, 'img': article_image})
            
            scraped_news.extend(articles)
            return articles

class PeopleScraper(Scraper):
    def __init__(self, topic = 'entertainment'):
        self.url = 'https://people.com/'+topic+'/'
        Scraper.__init__(self)

    async def scrape(self, async_client, scraped_news):
        async with async_client.get(self.url, headers=self.headers) as response:
            articles = []
            response_text = await response.text()
            soup = BeautifulSoup(response_text, 'html.parser')
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
            
            scraped_news.extend(articles)
            return articles