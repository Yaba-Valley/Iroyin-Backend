import requests
from bs4 import BeautifulSoup
from .base import Scraper


class FreeCodeCampScraper(Scraper):

    def __init__(self) -> None:
        self.url = 'https://www.freecodecamp.org'
        self.title = 'FreeCodeCamp'
        self.favicon_url = 'https://cdn.freecodecamp.org/universal/favicons/favicon.ico'

        Scraper.__init__(self)

    async def scrape(self, async_client, scraped_news):
        async with async_client.get(self.url + '/news', headers=self.headers) as response:
            html_text = await response.text()
            soup = BeautifulSoup(html_text, 'html.parser')
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
                                article_url, 'img': article_image, 'metadata': {'website': self.title, 'favicon': self.favicon_url}})

            scraped_news.extend(articles)
            return articles


class TechCrunchScraper(Scraper):
    def __init__(self, isNigeria, isStartups):
        
        if isNigeria:
            self.url = 'https://techcrunch.com/tag/nigeria'
        
        if isStartups:
            self.url = 'https://techcrunch.com/startups'
            
        self.title = 'TechCrunch'
        self.favicon_url = 'https://techcrunch.com/wp-content/uploads/2015/02/cropped-cropped-favicon-gradient.png?w=60'

        Scraper.__init__(self)

    async def scrape(self, async_client, scraped_news):
        async with async_client.get(self.url, headers=self.headers) as response:
            html_text = await response.text()
            soup = BeautifulSoup(html_text, 'html.parser')

            news = soup.find_all('article')

            articles = []

            for article in news:
                article_title = article.find(
                    'a', {'class': 'post-block__title__link'}).text
                article_url = article.find(
                    'a', {'class': 'post-block__title__link'})['href']
                article_image = article.find('img')['src']

                articles.append(
                    {'title': article_title.strip(), 'url': article_url, 'img': article_image, 'metadata': {'website': self.title, 'favicon': self.favicon_url}})

            scraped_news.extend(articles)
            return articles


class TechTrendsAfricaScraper(Scraper):
    def __init__(self, category):
        
        """
        category can either be 'tech-and-innovation', 'business',
        'funding', 'startups', '5g-and-the-internet-of-things', 'gadgets-apps',
        'blockchain' 
        """
        
        if category:
            self.url = 'https://techtrends.africa/category/'+category
        else:
            self.url = 'https://techtrends.africa'
            
        self.title = 'Tech Trends Africa'
        self.favicon_url = 'https://i0.wp.com/techtrends.africa/wp-content/uploads/2021/05/cropped-TechTrends.Africa-Logo-2.png?fit=192%2C192'

        Scraper.__init__(self)

    async def scrape(self, async_client, scraped_news):
        async with async_client.get(self.url, headers=self.headers) as response:
            html_text = await response.text()
            soup = BeautifulSoup(html_text, 'html.parser')

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
                    {'title': article_title.strip(), 'url': article_url, 'img': article_image.split('?')[0], 'metadata': {'website': self.title, 'favicon': self.favicon_url}})

            scraped_news.extend(articles)
            return articles


class GizModoScraper:
    def __init__(self):
        self.url = 'https://gizmodo.com/'
        self.title = 'Gizmodo'
        self.favicon_url = 'https://i.kinja-img.com/gawker-media/image/upload/h_60,w_60/fdj3buryz5nuzyf2k620.png'

    async def scrape(self, async_client, scraped_news):
        async with async_client.get(self.url) as response:
            html_text = await response.text()
            soup = BeautifulSoup(html_text, 'html.parser')

            news = soup.find_all('article')

            articles = []

            for article in news:
                try:
                    article_title = article.select_one('h4').text
                    article_url = article.select_one('a')['href']
                    article_image = article.select_one('img')['src']

                    articles.append({'title': article_title.strip(),
                                    'img': article_image, 'url': article_url, 'metadata': {'website': self.title, 'favicon': self.favicon_url}})

                except:
                    continue

            scraped_news.extend(articles)
            return articles


class TheNextWebScraper:

    """
    categories = ['latest', 'plugged', 'neural', 'shift',
                  'growth-quarters', 'hardfork', 'house-of-talent',
                  'future-of-finance', 'readme'
                  ]
    """

    def __init__(self, category='latest') -> None:
        self.category = category
        self.url = 'https://thenextweb.com/'
        self.title = 'The Next Web'
        self.favicon_url = 'https://next.tnwcdn.com/assets/img/favicon/favicon-194x194.png'

    async def scrape(self, async_client, scraped_news):

        articles = []
        async with async_client.get(self.url + self.category) as response:
            html_text = await response.text()
            soup = BeautifulSoup(html_text, 'html.parser')

            news = soup.select('article')

            try:
                for article in news:
                    if article.select_one('.c-card__heading') == None:
                        article_title = article.select_one('h4').text.strip()
                        article_url = self.url + article.select_one('a')['href'][1:]   
                        article_image = article.select_one('img')['src']

                        articles.append(
                            {'title': article_title, 'url': article_url, 'img': article_image, 'metadata': {'website': self.title, 'favicon': self.favicon_url}})
                        
                    else:
                        article_title = article.select_one('h3').text.strip()
                        article_url = self.url + article.select_one('a')['href']
                        article_image = article.select_one('img')['data-src']

                        articles.append(
                            {'title': article_title, 'url': article_url, 'img': article_image, 'metadata': {'website': self.title, 'favicon': self.favicon_url}})
                        
            except Exception as e:
                print(e)
                pass

            scraped_news.extend(articles)
            return articles


class GlassDoorScraper:
    def __init__(self) -> None:
        self.url = 'https://glassdoor.com'
        self.title = 'GlassDoor'
        self.favicon_url = 'https://www.glassdoor.com/favicon.ico'

    async def scrape(self, async_client, scraped_news):
        articles = []

        async with async_client.get(self.url + '/blog') as response:
            html_text = await response.text()
            soup = BeautifulSoup(html_text, 'html.parser')

            for article in soup.select('.post'):
                article_title = article.select_one('h3').text
                article_url = self.url + article.select_one('a')['href']
                article_image = article.select_one(
                    '.css-6uzs0z')['style'].split('url(')[1].split(')')[0]

                articles.append(
                    {'title': article_title, 'img': article_image, 'url': article_url, 'metadata': {'website': self.title, 'favicon': self.favicon_url}})

            for article in soup.select('.featured-article'):
                article_title = article.select_one('h2').text
                article_url = article.select_one('a')['href']
                article_image = article.select_one('img')['src']

                articles.append(
                    {'title': article_title, 'img': article_image, 'url': article_url, 'metadata': {'website': self.title, 'favicon': self.favicon_url}})

            scraped_news.extend(articles)
            return articles


class NewsBlockScraper(Scraper):
    def __init__(self):
        self.url = 'https://newblock.news/'
        self.title = 'NewsBlock'
        self.favicon_url = 'https://newblock.news/wp-content/uploads/2022/01/cropped-webicon-192x192.png'
        Scraper.__init__(self)

    async def scrape(self, async_client, scraped_news):
        async with async_client.get(self.url, headers=self.headers) as response:
            html_text = await response.text()
            soup = BeautifulSoup(html_text, 'html.parser')

            news = soup.find_all('article')

            articles = []

            for article in news:
                try:
                    article_title = article.find('h3').text
                    article_image = article.find('img')['data-src']
                    article_url = article.find('a')['href']
                    articles.append(
                        {'title': article_title, 'url': article_url, 'img': article_image, 'metadata': {'website': self.title, 'favicon': self.favicon_url}})
                except:
                    pass

            scraped_news.extend(articles)
            return articles

