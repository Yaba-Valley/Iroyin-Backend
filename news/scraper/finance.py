from .base import Scraper
from bs4 import BeautifulSoup
import requests
from markdownify import markdownify as md


class FinanceSamuraiScraper(Scraper):
    def __init__(self):
        self.url = 'https://www.financialsamurai.com/'
        self.title = 'FinanceSamurai'
        self.favicon = 'https://i2.wp.com/financialsamurai.com/wp-content/uploads/2017/02/cropped-FinancialSamurai-Site-Icon-700x700-180x180.png'

        super().__init__(self.title)

    async def scrape(self, async_client, scraped_news, failed_scrapers):
        try:
            print('scraping', self.url)
            async with async_client.get(self.url, headers=self.headers) as response:
                articles = []
                response_text = await response.text()
                soup = BeautifulSoup(response_text, 'html.parser')

                for article in soup.find_all("article"):
                    try:
                        article_title = article.find(
                            'h2', class_='entry-title').text
                        print(article.find('img'))
                        srcset = article.find('img').attrs.get(
                            'data-lazy-srcset')
                        print(srcset)
                        article_image = srcset.split(', ')[-1].split(' ')[0]
                        article_url = article.find('a')['href']

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
        text_content = soup.find('div', class_='entry-content')

        return md(str(text_content))


class InvestopediaScraper(Scraper):
    def __init__(self, topic='company-news'):
        """ 
        topic can either be: 

        company-news,
        market-news,
        crypto-news,
        personal-finance-news,
        economic-news,
        political-news,
        """

        if topic == 'company-news':
            self.url = 'https://www.investopedia.com/company-news-4427705'
        elif topic == 'market-news':
            self.url = 'https://www.investopedia.com/markets-news-4427704'
        elif topic == 'crypto-news':
            self.url = 'https://www.investopedia.com/cryptocurrency-news-5114163'
        elif topic == 'personal-finance-news':
            self.url = 'https://www.investopedia.com/personal-finance-news-5114159'
        elif topic == 'economic-news':
            self.url = 'https://www.investopedia.com/economic-news-5218422'
        elif topic == 'political-news':
            self.url = 'https://www.investopedia.com/political-news-4689737'
        else:
            self.url = 'https://www.investopedia.com/company-news-4427705'

        self.title = 'Investopedia'
        self.favicon = 'https://www.investopedia.com/favicon.ico'

        super().__init__(self.title)

    async def scrape(self, async_client, scraped_news, failed_scrapers):
        try:
            print('scraping', self.url)
            async with async_client.get(self.url, headers=self.headers) as response:
                articles = []
                response_text = await response.text()
                soup = BeautifulSoup(response_text, 'html.parser')

                print(len(soup.find_all("a", class_="mntl-card")))

                for article in soup.find_all("a", class_="mntl-card"):
                    try:
                        article_title = article.find(
                            'span', class_='card__title').text
                        article_image = article.find(
                            'img').attrs.get('data-src')
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
        text_content = soup.find('div', class_='comp article-body-content mntl-sc-page mntl-block')

        return md(str(text_content))


class ForbesScraper(Scraper):
    def __init__(self, category='news'):
        
        """ 
        category can be either of the following:
        real-estate, leadership, money, lifestyle, innovation, business, small-business, world-billionaires
        """
        self.url = f'https://www.forbes.com/{category}/'
        self.title = 'Forbes'
        self.favicon = 'https://i.forbesimg.com/48X48-F.png'
        super().__init__(self.title)


    async def scrape(self, async_client, scraped_news, failed_scrapers):
        try:
            print('scraping', self.url)
            async with async_client.get(self.url, headers=self.headers) as response:
                articles = []
                response_text = await response.text()
                soup = BeautifulSoup(response_text, 'html.parser')

                for article in soup.find_all("article"):
                    try:
                        article_title = article.find(
                            'a', class_='stream-item__title').text
                        article_url = article.find(
                            'a', class_='stream-item__title')['href']
                        article_image = article.find(
                            'a', class_='stream-item__image').attrs.get('style').split("url(\"")[1].split('?')[0]

                        articles.append(
                            {'title': article_title, 'url': article_url, 'img': article_image, 'metadata': {'website': self.title, 'favicon': self.favicon}})
                    except Exception as e:
                        print(e)

                for article in soup.find_all('div', class_='card'):
                    try:
                        article_title = article.find('h2').text
                        article_url = article.find('a')['href']
                        article_image = article.find(
                            'progressive-image').attrs.get('background-image').split('?')[0]

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
        text_content = soup.find('div', class_='article-body')

        return md(str(text_content))
