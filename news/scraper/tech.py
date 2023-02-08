from bs4 import BeautifulSoup
from .base import Scraper
import requests
from markdownify import markdownify as md


class FreeCodeCampScraper(Scraper):

    def __init__(self) -> None:
        self.url = 'https://www.freecodecamp.org'
        self.title = 'FreeCodeCamp'
        self.favicon_url = 'https://cdn.freecodecamp.org/universal/favicons/favicon.ico'

        Scraper.__init__(self, 'FreeCodeCamp Scraper')

    async def scrape(self, async_client, scraped_news, failed_scrapers):
        try:
            print(self.url + '/news')
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
                # print(articles)
                return articles
        except Exception as e:
            print(self.url + '/news is not working')
            failed_scrapers.append({ 'url': self.url, 'error': str(e) })
            pass

    def scrape_news_content(self, url):
        res_text = requests.get(url=url).text
        soup = BeautifulSoup(res_text, 'html.parser')
        article_content = soup.find('section', class_='post-content')

        return md(str(article_content))


class TechCrunchScraper(Scraper):
    def __init__(self, category='plus'):
        """ 
        category can be any of the following:
        [plus, startups, venture, security, crypto, apps, fintech, hardware, transportation, entertainment, nigeria]
        """
        if category == 'plus':
            self.url = 'https://techcrunch.com/techcrunchplus'
        elif category == 'startups':
            self.url = 'https://techcrunch.com/category/startups/'
        elif category == 'venture':
            self.url = 'https://techcrunch.com/category/venture/'
        elif category == 'security':
            self.url = 'https://techcrunch.com/category/security/'
        elif category == 'crypto':
            self.url = 'https://techcrunch.com/category/cryptocurrency/'
        elif category == 'apps':
            self.url = 'https://techcrunch.com/category/apps/'
        elif category == 'fintech':
            self.url = 'https://techcrunch.com/category/fintech/'
        elif category == 'hardware':
            self.url = 'https://techcrunch.com/category/hardware/'
        elif category == 'transportation':
            self.url = 'https://techcrunch.com/category/transportation/'
        elif category == 'entertainment':
            self.url = 'https://techcrunch.com/category/media-entertainment/'
        else:
            self.url = 'https://techcrunch.com/tag/nigeria'

        self.title = 'TechCrunch'
        self.favicon_url = 'https://techcrunch.com/wp-content/uploads/2015/02/cropped-cropped-favicon-gradient.png?w=60'

        Scraper.__init__(self, 'TechCrunch Scraper')

    async def scrape(self, async_client, scraped_news, failed_scrapers):
        try:
            print(self.url)
            async with async_client.get(self.url, headers=self.headers) as response:
                html_text = await response.text()
                soup = BeautifulSoup(html_text, 'html.parser')
                all_articles = soup.find_all('div', {'class': 'post-block'})

                articles = []

                for article in all_articles:

                    article_title_element = article.find(
                        'a', {'class': 'post-block__title__link'})
                    article_title = ''

                    if article_title_element is not None:
                        article_title = article_title_element.text

                    article_url_element = article.find(
                        'a', {'class': 'post-block__title__link'})
                    article_url = ''

                    if article_url_element is not None:
                        article_url = article_title_element['href']

                    article_image_element = article.find('img')
                    article_image = ''

                    if article_image_element is not None:
                        article_image = article_image_element['src']

                    articles.append(
                        {'title': article_title.strip(), 'url': article_url, 'img': article_image, 'metadata': {'website': self.title, 'favicon': self.favicon_url}})

                scraped_news.extend(articles)
                return scraped_news
        except Exception as e:
            print(self.url + ' is not working')
            failed_scrapers.append({ 'url': self.url, 'error': str(e) })
            pass

    def scrape_news_content(self, url):
        response_text = requests.get(url, headers=self.headers).text
        soup = BeautifulSoup(response_text, 'html.parser')

        featured_img = soup.find('img', class_='article__featured-image')
        article_content = soup.find('div', class_='article-content')

        return md(str(featured_img) + str(article_content))


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

        Scraper.__init__(self, 'Tech Trends Scraper')

    async def scrape(self, async_client, scraped_news, failed_scrapers):
        try:
            print(self.url)
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
                # print(articles)
                return articles
        except Exception as e:
            print(self.url + ' is not working')
            failed_scrapers.append({ 'url': self.url, 'error': str(e) })
            pass

    def scrape_news_content(self, url):
        res_text = requests.get(url=url).text
        soup = BeautifulSoup(res_text, 'html.parser')
        article_content = soup.find(
            'div', class_='content-inner  jeg_link_underline')

        return md(str(article_content))


class GizModoScraper:
    def __init__(self):
        self.url = 'https://gizmodo.com/'
        self.title = 'Gizmodo'
        self.favicon_url = 'https://i.kinja-img.com/gawker-media/image/upload/h_60,w_60/fdj3buryz5nuzyf2k620.png'

        Scraper.__init__(self, 'GizModo Scraper')

    async def scrape(self, async_client, scraped_news, failed_scrapers):
        try:
            print(self.url)
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
        except Exception as e:
            print(self.url + ' is not working')
            failed_scrapers.append({ 'url': self.url, 'error': str(e) })
            pass


class TheNextWebScraper(Scraper):

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

        Scraper.__init__(self, 'TheNextWeb Scraper')

    async def scrape(self, async_client, scraped_news, failed_scrapers):
        try:
            print(self.url + self.category)
            articles = []
            async with async_client.get(self.url + self.category) as response:
                html_text = await response.text()
                soup = BeautifulSoup(html_text, 'html.parser')

                all_articles = soup.find_all('article')

                try:
                    for article in all_articles:
                        if ''.join(article.attrs['class']).find('c-listArticle') != -1:
                            article_title = article.select_one(
                                'h4').text.strip()
                            article_url = self.url + \
                                article.select_one('h4').find('a')['href']
                            article_image = article.select_one('img').attrs.get(
                                'data-src') or article.select_one('img').attrs.get('src')

                            articles.append(
                                {'title': article_title, 'url': article_url, 'img': article_image, 'metadata': {'website': self.title, 'favicon': self.favicon_url}})

                        else:
                            article_title = article.select_one(
                                'h3').text.strip()
                            article_url = self.url + \
                                article.select_one('a')['href']
                            article_image = article.select_one('img').attrs.get(
                                'data-src') or article.select_one('img').attrs.get('src')

                            articles.append(
                                {'title': article_title, 'url': article_url, 'img': article_image, 'metadata': {'website': self.title, 'favicon': self.favicon_url}})

                except Exception as e:
                    pass

                scraped_news.extend(articles)
                return scraped_news
        except Exception as e:
            print(self.url + ' is not working')
            failed_scrapers.append({ 'url': self.url, 'error': str(e) })
            pass

    def scrape_news_content(self, url):
        response_text = requests.get(url=url).text
        soup = BeautifulSoup(response_text, 'html.parser')

        article_content = soup.find(
            'main', class_='c-article__main max-lg:mb-xxl')

        return md(str(article_content))


class GlassDoorScraper:
    def __init__(self) -> None:
        self.url = 'https://glassdoor.com'
        self.title = 'GlassDoor'
        self.favicon_url = 'https://www.glassdoor.com/favicon.ico'

        Scraper.__init__(self, 'GlassDoor Scraper')

    async def scrape(self, async_client, scraped_news, failed_scrapers):
        try:
            articles = []
            print(self.url + '/blog')
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
                # print(articles)
                return articles
        except Exception as e:
            print(self.url + ' is not working')
            failed_scrapers.append({ 'url': self.url, 'error': str(e) })
            pass

    def scrape_news_content(self, url):
        response_text = requests.get(url).text
        soup = BeautifulSoup(response_text)
        article = soup.find('article', class_='article css-avgnsc css-vtrr42')
        return md(str(article))


class NewsBlockScraper(Scraper):
    def __init__(self):
        self.url = 'https://newblock.news/'
        self.title = 'NewsBlock'
        self.favicon_url = 'https://newblock.news/wp-content/uploads/2022/01/cropped-webicon-192x192.png'
        Scraper.__init__(self, 'NewsBlock Scraper')

    async def scrape(self, async_client, scraped_news, failed_scrapers):
        try:
            print(self.url)
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
                # print(articles)
                return articles
        except Exception as e:
            print(self.url + ' is not working')
            failed_scrapers.append({ 'url': self.url, 'error': str(e) })
            pass


class BitcoinNewsScraper(Scraper):
    def __init__(self) -> None:
        Scraper.__init__(self, 'Bitcoin News')
        self.url = 'https://news.bitcoin.com'
        self.title = 'Bitcoin News'
        self.favicon_url = 'https://static.news.bitcoin.com/wp-content/uploads/2019/07/favicon-3.png'
        
        
    async def scrape(self, async_client, scraped_news, failed_scrapers):
        try:
            articles = []
            print(self.url)
            async with async_client.get(self.url) as response:
                html_text = await response.text()
                soup = BeautifulSoup(html_text, 'html.parser')

                for article in soup.select('.story'):
                    article_title = article.find('h6')
                    if article_title is not None:
                        article_title = article_title.text;
                    else:
                        article_title = article.find('h5').text
                        
                        
                    article_url = article.find('a')['href']
                    article_image = article.find('img')
                                        
                    if article_image is None:
                        article_image = ''
                    else:
                        article_image = article_image.attrs.get('srcset').split(', ')[-1].split(' ')[0]

                    print(article_title, article_image, article_url)
                    
                    articles.append(
                        {'title': article_title, 'img': article_image, 'url': article_url, 'metadata': {'website': self.title, 'favicon': self.favicon_url}})

                scraped_news.extend(articles)
                return articles
        except Exception as e:
            print(self.url + ' is not working')
            failed_scrapers.append({ 'url': self.url, 'error': str(e) })
            pass

    def scrape_news_content(self, url):
        response_text = requests.get(url).text
        soup = BeautifulSoup(response_text)
        article = soup.find('article', class_='article css-avgnsc css-vtrr42')
        return md(str(article))


