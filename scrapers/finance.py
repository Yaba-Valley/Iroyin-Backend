from .base import Scraper
from bs4 import BeautifulSoup
import requests
from markdownify import markdownify as md
from .myscrape import scraper


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
                # soup = BeautifulSoup(response_text, 'html.parser')

                scraper(
                    website_text=response_text,
                    website_name=self.title,
                    favicon=self.favicon,
                    smallest_article_element='article',
                    class_of_smallest_article_element='post',
                    smallest_title_element='h2',
                    class_of_smallest_title_element='entry-title',
                    smallest_link_element_with_class='h2',
                    class_of_smallest_link_element='entry-title',
                    image_holder_attr='data-lazy-srcset',
                    smallest_image_element='img',
                    class_of_smallest_image_element='entry-image attachment-post'
                )

                scraped_news.extend(articles)
                print(articles)
                return scraped_news
        except Exception as e:
            print(self.url, 'is not working', e)
            failed_scrapers.append({'url': self.url, 'error': str(e)})
            pass

    def scrape_news_content(self, url):
        res_text = requests.get(url).text
        soup = BeautifulSoup(res_text, 'html.parser')

        scripts = soup.find_all('script')

        for script in scripts:
            script.decompose()

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
                # soup = BeautifulSoup(response_text, 'html.parser')

                articles = scraper(website_text=response_text,
                                   website_name=self.title,
                                   favicon=self.favicon,
                                   smallest_article_element='a',
                                   class_of_smallest_article_element='mntl-card',
                                   smallest_link_element_with_class='a',
                                   class_of_smallest_link_element='mntl-card',
                                   smallest_image_element='img',
                                   class_of_smallest_image_element='img--noscript card__img universal-image__image',
                                   smallest_title_element='span',
                                   class_of_smallest_title_element='card__title-text',
                                   image_holder_attr='src'
                                   )

                scraped_news.extend(articles)
                return scraped_news
        except Exception as e:
            print(self.url, 'is not working', e)
            failed_scrapers.append({'url': self.url, 'error': str(e)})
            pass

    def scrape_news_content(self, url):
        res_text = requests.get(url).text
        soup = BeautifulSoup(res_text, 'html.parser')

        scripts = soup.find_all('script')

        for script in scripts:
            script.decompose()

        text_content = soup.find(
            'div', class_='comp article-body-content mntl-sc-page mntl-block')

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

        scripts = soup.find_all('script')

        for script in scripts:
            script.decompose()

        text_content = soup.find('div', class_='article-body')

        return md(str(text_content), strip=['script, iframe'])
