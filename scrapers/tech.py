from bs4 import BeautifulSoup
from .base import Scraper
import requests
from markdownify import markdownify as md
from .myscrape import scraper


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

                news = scraper(website_text=html_text,
                               smallest_article_element='article',
                               class_of_smallest_article_element='post-card',
                               smallest_title_element='h2',
                               class_of_smallest_title_element='post-card-title',
                               smallest_link_element_with_class='a',
                               class_of_smallest_link_element='post-card-image-link',
                               smallest_image_element='a',
                               class_of_smallest_image_element='post-card-image-link',
                               image_holder_attr='srcset',
                               prepend_url='https://freecodecamp.com/news',
                               website_name=self.title,
                               favicon=self.favicon_url
                               )

                scraped_news.extend(news)
                return news
        except Exception as e:
            print(self.url + '/news is not working')
            failed_scrapers.append({'url': self.url, 'error': str(e)})
            pass

    def scrape_news_content(self, url):
        res_text = requests.get(url=url).text
        soup = BeautifulSoup(res_text, 'html.parser')

        scripts = soup.find_all('script')

        for script in scripts:
            script.decompose()

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

                news = scraper(website_name=self.title,
                               website_text=html_text,
                               smallest_article_element='div',
                               class_of_smallest_article_element='post-block post-block--image post-block--unread',
                               smallest_link_element_with_class='a',
                               class_of_smallest_link_element='post-block__title__link',
                               smallest_image_element='img',
                               class_of_smallest_image_element=None,
                               smallest_title_element='a',
                               class_of_smallest_title_element='post-block__title__link',
                               favicon=self.favicon_url,
                               image_holder_attr='src'
                               )

                scraped_news.extend(news)
                return news
        except Exception as e:
            print(self.url + ' is not working')
            failed_scrapers.append({'url': self.url, 'error': str(e)})
            pass

    def scrape_news_content(self, url):
        response_text = requests.get(url, headers=self.headers).text
        soup = BeautifulSoup(response_text, 'html.parser')

        scripts = soup.find_all('script')

        for script in scripts:
            script.decompose()

        article_content = soup.find('div', class_='article-content')

        return md(str(article_content))


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

                articles = scraper(website_text=html_text,
                                   smallest_article_element='article',
                                   class_of_smallest_article_element='jeg_post jeg_pl_lg_2 format-standard',
                                   smallest_link_element_with_class='h3',
                                   class_of_smallest_link_element='jeg_post_title',
                                   smallest_title_element='h3',
                                   class_of_smallest_title_element='jeg_post_title',
                                   image_holder_attr='data-src',
                                   class_of_smallest_image_element='thumbnail-container animate-lazy size-715',
                                   smallest_image_element='div',
                                   website_name=self.title,
                                   favicon=self.favicon_url
                                   )

                scraped_news.extend(articles)
                return articles
        except Exception as e:
            print(self.url + ' is not working')
            print(e)
            failed_scrapers.append({'url': self.url, 'error': str(e)})
            pass

    def scrape_news_content(self, url):
        res_text = requests.get(url=url).text
        soup = BeautifulSoup(res_text, 'html.parser')

        scripts = soup.find_all('script')

        for script in scripts:
            script.decompose()

        article_content = soup.find(
            'div', class_='content-inner  jeg_link_underline')

        return md(str(article_content))


class GizModoScraper:
    def __init__(self, category=''):
        self.url = 'https://gizmodo.com/'
        self.title = 'Gizmodo'
        self.category = category
        self.favicon_url = 'https://i.kinja-img.com/gawker-media/image/upload/h_60,w_60/fdj3buryz5nuzyf2k620.png'

        Scraper.__init__(self, 'GizModo Scraper')

    async def scrape(self, async_client, scraped_news, failed_scrapers):
        try:
            print(self.url + self.category)
            async with async_client.get(self.url + self.category) as response:
                html_text = await response.text()

                articles = scraper(website_text=html_text,
                                   website_name=self.title,
                                   favicon=self.favicon_url,
                                   smallest_article_element='article',
                                   class_of_smallest_article_element='sc-1pw4fyi-6 laejkp sc-1e59qvl-0 sc-1e59qvl-1 yrIlL gwBFdc js_post_item',
                                   smallest_link_element_with_class='a',
                                   class_of_smallest_link_element='sc-1out364-0 dPMosf sc-1pw4fyi-5 eJvgGf js_link',
                                   smallest_image_element='img',
                                   class_of_smallest_image_element='',
                                   smallest_title_element='h4',
                                   class_of_smallest_title_element='sc-1qoge05-0 nvHxA',
                                   image_holder_attr='src'
                                   )

                scraped_news.extend(articles)
                return articles
        except Exception as e:
            print(self.url + ' is not working', e)
            failed_scrapers.append({'url': self.url, 'error': str(e)})
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
            async with async_client.get(self.url + self.category) as response:
                html_text = await response.text()
                articles = scraper(
                    website_text=html_text,
                    website_name=self.title,
                    favicon=self.favicon_url,
                    smallest_article_element='article',
                    class_of_smallest_article_element='c-listArticle',
                    image_holder_attr='srcset',
                    smallest_image_element='noscript',
                    class_of_smallest_image_element=None,
                    smallest_link_element_with_class='a',
                    class_of_smallest_link_element='title_link',
                    smallest_title_element='h4',
                    class_of_smallest_title_element='c-listArticle__heading'
                )

                scraped_news.extend(articles)
                return scraped_news
        except Exception as e:
            print(self.url + ' is not working')
            failed_scrapers.append({'url': self.url, 'error': str(e)})
            pass

    def scrape_news_content(self, url):
        response_text = requests.get(url=url).text
        soup = BeautifulSoup(response_text, 'html.parser')

        scripts = soup.find_all('script')

        for script in scripts:
            script.decompose()

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
                articles = scraper(website_text=html_text,
                                   website_name=self.title,
                                   favicon=self.favicon_url,
                                   smallest_article_element='div',
                                   class_of_smallest_article_element='post',
                                   smallest_image_element='div',
                                   class_of_smallest_image_element='css-6uzs0z',
                                   image_holder_attr='style',
                                   smallest_link_element_with_class='a',
                                   class_of_smallest_link_element='d-flex flex-column css-y96yjg',
                                   class_of_smallest_title_element=None,
                                   smallest_title_element='h3',
                                   prepend_url=self.url)

                scraped_news.extend(articles)
                print(articles)
                return articles
        except Exception as e:
            print(self.url + ' is not working')
            failed_scrapers.append({'url': self.url, 'error': str(e)})
            pass

    def scrape_news_content(self, url):
        response_text = requests.get(url).text
        soup = BeautifulSoup(response_text)

        scripts = soup.find_all('script')

        for script in scripts:
            script.decompose()

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
            failed_scrapers.append({'url': self.url, 'error': str(e)})
            pass


class BitcoinNewsScraper(Scraper):
    def __init__(self) -> None:
        Scraper.__init__(self, 'Bitcoin News')
        self.url = 'https://news.bitcoin.com'
        self.title = 'Bitcoin News'
        self.favicon_url = 'https://static.news.bitcoin.com/wp-content/uploads/2019/07/favicon-3.png'

    async def scrape(self, async_client, scraped_news, failed_scrapers):
        try:
            print(self.url)
            async with async_client.get(self.url) as response:
                html_text = await response.text()

                articles = scraper(website_name=self.title,
                                   favicon=self.favicon_url,
                                   website_text=html_text,
                                   smallest_article_element='div',
                                   class_of_smallest_article_element='story',
                                   smallest_image_element='img',
                                   class_of_smallest_image_element='story__img',
                                   smallest_link_element_with_class='a',
                                   class_of_smallest_link_element='',
                                   smallest_title_element='h6',
                                   class_of_smallest_title_element='story__title',
                                   image_holder_attr='srcset'
                                   )

                scraped_news.extend(articles)
                return articles
        except Exception as e:
            print(self.url + ' is not working')
            failed_scrapers.append({'url': self.url, 'error': str(e)})
            pass

    def scrape_news_content(self, url):
        response_text = requests.get(url).text
        soup = BeautifulSoup(response_text, 'html.parser')

        scripts = soup.find_all('script')

        for script in scripts:
            script.decompose()

        article = soup.find('article', class_='article css-avgnsc css-vtrr42')
        return md(str(article))


class QuartzScraper(Scraper):
    """ 
    category is either [
        latest,finance-and-investing,economics,technology,sustainability,lifestyle,work
    ]
    """

    def __init__(self, category='latest') -> None:
        Scraper.__init__(self, 'Quartz')
        self.url = 'https://qz.com/'
        self.title = 'Quartz'
        self.category = category
        self.favicon_url = 'https://i.kinja-img.com/gawker-media/image/upload/c_fill,f_auto,fl_progressive,g_center,h_80,q_80,w_80/4716932d29f4ef6064940c18eaab1f3d.png'

    async def scrape(self, async_client, scraped_news, failed_scrapers):
        try:
            print(self.url + self.category)
            async with async_client.get(self.url + self.category) as response:
                html_text = await response.text()

                articles = scraper(
                    website_name=self.title,
                    favicon=self.favicon_url,
                    website_text=html_text,
                    smallest_article_element='article',
                    class_of_smallest_article_element='js_post_item',
                    smallest_title_element='h2',
                    class_of_smallest_title_element='sc-759qgu-0 cwUChs sc-cw4lnv-6 lgbIVS',
                    smallest_link_element_with_class='a',
                    class_of_smallest_link_element='sc-1out364-0 dPMosf js_link',
                    smallest_image_element='picture',
                    class_of_smallest_image_element='lazy-picture',
                    image_holder_attr='data-src'
                )

                scraped_news.extend(articles)
                return articles
        except Exception as e:
            print(self.url + ' is not working')
            failed_scrapers.append({'url': self.url, 'error': str(e)})
            pass

    def scrape_news_content(self, url):
        response_text = requests.get(url).text
        soup = BeautifulSoup(response_text, 'html.parser')

        scripts = soup.find_all('script')

        for script in scripts:
            script.decompose()

        article = soup.find('div', id='js_movable-ads-post-contents')
        return md(str(article))


class AxiosScraper(Scraper):
    def __init__(self) -> None:
        Scraper.__init__(self, 'Axios')
        self.url = 'https://www.axios.com/'
        self.title = 'Axios'
        self.favicon_url = 'https://www.axios.com/images/a_favicon-228.png'

    async def scrape(self, async_client, scraped_news, failed_scrapers):
        try:
            print(self.url)
            async with async_client.get(self.url) as response:
                html_text = await response.text()

                articles = scraper(website_text=html_text,
                                   website_name=self.title,
                                   favicon=self.favicon_url,
                                   smallest_article_element='div',
                                   class_of_smallest_article_element='gtmView grid-layout border-b border-accent-blue-tint pb-6 sm:pb-10 last:border-b-0',
                                   smallest_title_element='h2',
                                   class_of_smallest_title_element='col-1-13 m-0',
                                   smallest_link_element_with_class='h2',
                                   class_of_smallest_link_element='col-1-13 m-0',
                                   smallest_image_element='figure',
                                   class_of_smallest_image_element='StoryImage_caption__oW2Fs m-0 pt-6 col-1-13',
                                   image_holder_attr='srcset',
                                   prepend_url=self.url
                                   )

                scraped_news.extend(articles)
                return articles
        except Exception as e:
            print(self.url + ' is not working')
            failed_scrapers.append({'url': self.url, 'error': str(e)})
            pass

    def scrape_news_content(self, url):
        response_text = requests.get(url).text
        soup = BeautifulSoup(response_text, 'html.parser')

        scripts = soup.find_all('script')

        for script in scripts:
            script.decompose()

        article = soup.find('div', id='js_movable-ads-post-contents')
        return md(str(article))
