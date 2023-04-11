import requests
from bs4 import BeautifulSoup
from .base import Scraper
from markdownify import markdownify as md


class VanguardScraper(Scraper):
    def __init__(self, topic='sports') -> None:
        self.url = f'https://www.vanguardngr.com/category/{topic}/'

        Scraper.__init__(self, 'Vanguard Scraper')

    def scrape(self):

        # get big thumbnail news
        request = requests.get(self.url, headers=self.headers).content
        soup = BeautifulSoup(request, 'lxml')
        value = soup.find_all('h2', {'class': 'entry-title'})

        headlines = [
            {'title': i.text, 'url': i.find('a')['href']} for i in value]

        return headlines


class PunchScraper(Scraper):
    def __init__(self, topic='sports') -> None:
        self.url = f'https://punchng.com/topics/{topic}/'
        self.website = 'Punch NG'
        self.favicon = 'https://cdn.punchng.com/wp-content/uploads/2016/06/19220759/favicon.jpg'

        Scraper.__init__(self, 'Punch Scraper')

    async def scrape(self, async_client, scraped_news, failed_scrapers):
        try:
            async with async_client.get(self.url, headers=self.headers) as response:
                html_text = await response.text()
                soup = BeautifulSoup(html_text, 'html.parser')

                all_articles = soup.find_all('article')
                headlines = []

                for i in all_articles:
                    try:
                        img = i.find('img').attrs.get('data-src')
                        img_src_set = i.find('img').attrs.get('data-srcset')

                        if img_src_set:
                            last_src_set = img_src_set.split(', ')[-1]
                            img = last_src_set.split(' ')[0]

                        news = i.find('a').text.strip()
                        link = i.find('a')['href']
                        headlines.append({'title': news, 'url': link, 'img': img, 'metadata': {
                            'website': self.website, 'favicon': self.favicon}})
                    except:
                        img = 'https://cdn.punchng.com/wp-content/uploads/2021/05/16175056/IMG-20210516-WA0002.jpg'
                        news = i.find('a').text.strip()
                        link = i.find('a')['href']

                        print(img, news, link, self.url)
                        headlines.append({'title': news, 'url': link, 'img': img, 'metadata': {
                            'website': self.website, 'favicon': self.favicon}})

                scraped_news.extend(headlines)
                return scraped_news

        except Exception as e:
            print(self.url, 'is not working')
            failed_scrapers.append({'url': self.url, 'error': str(e)})
            pass


class GoalDotComScraper(Scraper):

    def __init__(self) -> None:
        self.url = 'https://www.goal.com'
        self.website = 'Goal.com'
        self.favicon = 'https://www.logodesignlove.com/images/sports/goal-logo-elmwood-01.jpg'

        Scraper.__init__(self, 'goal.com scraper')

    async def scrape(self, async_client, scraped_news, failed_scrapers):
        try:
            print(f'{self.url}/en-ng/news/1')

            async with async_client.get(self.url + '/en-ng/news/1') as response:
                html_text = await response.text()
                soup = BeautifulSoup(html_text, 'html.parser')
                value = soup.find_all('article')
                headlines = []

                for i in value:
                    try:
                        img = i.find('img').get('src').split('?')[0]
                        news = i.find('h3', class_='title h5').text
                        link = self.url+i.find('a')['href']
                        headlines.append({'title': news, 'url': link, 'img': img, 'metadata': {
                            'website': self.website, 'favicon': self.favicon}})
                    except Exception as e:
                        print(e)

                scraped_news.extend(headlines)
                return headlines
        except Exception as e:
            print(f'{self.url}/en-ng/news/1 is not working')
            failed_scrapers.append({'url': self.url, 'error': str(e)})
            pass

    def scrape_news_content(self, url):
        response_text = requests.get(url).text
        soup = BeautifulSoup(response_text, 'html.parser')

        scripts = soup.find_all('script')

        for script in scripts:
            script.decompose()

        text_content = soup.find('div', class_='article_content__XFYIz')

        return md(str(text_content))


class SkySportScraper(Scraper):
    def __init__(self) -> None:
        self.url = 'https://www.skysports.com/news-wire'
        self.website = 'Sky Sports'
        self.favicon = 'https://www.skysports.com/favicon.ico'

        Scraper.__init__(self, 'SkySport Scraper')

    async def scrape(self, async_client, scraped_news, failed_scrapers):
        try:
            print(self.url)
            async with async_client.get(self.url, headers=self.headers) as response:
                html_text = await response.text()
                soup = BeautifulSoup(html_text, 'html.parser')
                news = soup.find_all(
                    'div', {'class': 'news-list__item news-list__item--show-thumb-bp30'})

                headlines = [{'title': article.find('a', {'class': 'news-list__headline-link'}).text.strip(), 'url': article.find('a', {'class': 'news-list__headline-link'})['href'], 'img':article.find('img')['data-src'], 'metadata': {'favicon': self.favicon, 'website': self.website}}
                             for article in news]

                scraped_news.extend(headlines)
                return headlines
        except Exception as e:
            print(f'{self.url} is not working')
            failed_scrapers.append({'url': self.url, 'error': str(e)})
            pass

    def scrape_news_content(self, url):
        res_text = requests.get(url=url).text
        soup = BeautifulSoup(res_text, 'html.parser')

        scripts = soup.find_all('script')

        for script in scripts:
            script.decompose()

        article_content = soup.find(
            'div', class_='sdc-article-body sdc-article-body--lead')

        return md(str(article_content))


class EPLScraper(Scraper):
    def __init__(self) -> None:
        self.url = 'https://www.premierleague.com'
        self.title = "Premier League"
        self.favicon = 'https://s3.amazonaws.com/premierleague-static-files/premierleague/pl_icon.png'

        Scraper.__init__(self, 'EPL Scraper')

    async def scrape(self, async_client, scraped_news, failed_scrapers):
        try:
            print(f'{self.url}/news')

            async with async_client.get(self.url+'/news', headers=self.headers) as response:
                html_text = await response.text()
                soup = BeautifulSoup(html_text, 'html.parser')
                news = soup.find_all('a', {'class': 'thumbnail thumbLong'})

                headlines = [{'title': article.find('span', {'class': 'title'}).text, 'url': self.url +
                              article['href'], 'img':article.find('img')['src'].strip(), 'metadata': {'website': self.title, 'favicon': self.favicon}} for article in news]

                scraped_news.extend(headlines)
                return headlines
        except Exception as e:
            print(f'{self.url}/news is not working')
            failed_scrapers.append({'url': self.url, 'error': str(e)})
            pass

    def scrape_news_content(self, url):
        res_text = requests.get(url=url).text
        soup = BeautifulSoup(res_text, 'html.parser')

        scripts = soup.find_all('script')

        for script in scripts:
            script.decompose()

        article_content = soup.find('section', class_='standardArticle')
        return md(str(article_content))


class LaLigaScraper(Scraper):
    def __init__(self) -> None:
        # images of laliga cannot be scraped cause of it JS abi CSS sha
        self.url = 'https://www.laliga.com'
        self.title = 'Laliga'
        self.favicon_url = 'https://assets.laliga.com/assets/public/logos/favicon.ico'

        Scraper.__init__(self, 'LaLiga Scraper')

    async def scrape(self, async_client, scraped_news, failed_scrapers):
        try:
            print(self.url + '/en-ES/news')
            async with async_client.get(self.url + '/en-ES/news') as response:
                html_text = await response.text()
                soup = BeautifulSoup(html_text, 'html.parser')

                news = soup.find_all(
                    'div', {'class': 'styled__ImageContainer-sc-1si1tif-0'})

                articles = []

                try:
                    for article in news:
                        title = article.find('h3').text
                        url = self.url + article.find('a')['href']
                        img = 'https://assets.laliga.com/assets/2019/10/09/medium/47d73a0eff4508d03ea51f26384bcba2.jpeg'
                        articles.append({'title': title, 'url': url, 'img': img, 'metadata': {
                                        'website': self.title, 'favicon': self.favicon_url}})
                except Exception as e:
                    print(e)
                    pass

                scraped_news.extend(articles)
                return articles
        except Exception as e:
            print(f'{self.url}/en-ES/news is not working')
            failed_scrapers.append({'url': self.url, 'error': str(e)})
            pass


class BundesligaScraper(Scraper):
    def __init__(self) -> None:
        self.url = 'https://www.bundesliga.com'
        self.title = 'Bundesliga'
        self.favicon_url = 'https://www.bundesliga.com/assets/favicons/android-chrome-192x192.png'

        Scraper.__init__(self, 'Bundesliga Scraper')

    async def scrape(self, async_client, scraped_news, failed_scrapers):
        try:
            print(self.url + '/en/bundesliga')
            async with async_client.get(self.url + '/en/bundesliga', headers=self.headers) as response:

                articles = []
                html_text = await response.text()
                soup = BeautifulSoup(html_text, 'html.parser')
                news = soup.select('.teaser')
                other_news = soup.select('.topListEntry')

                for article in news:
                    try:
                        article_title = article.find('h2').text
                        article_url = self.url + article.find('a')['href']
                        article_image = article.find(
                            'img')['src'].split('?')[0]

                        articles.append(
                            {'title': article_title.strip(), 'url': article_url, 'img': article_image, 'metadata': {'website': self.title, 'favicon': self.favicon_url}})
                    except Exception as e:
                        print(e)
                        pass

                for article in other_news:
                    try:
                        article_title = article.text
                        article_url = self.url + article['href']
                        article_image = article.find(
                            'img')['src'].split('?')[0]

                        articles.append(
                            {'title': article_title.strip(), 'url': article_url, 'img': article_image, 'metadata': {'website': self.title, 'favicon': self.favicon_url}})
                    except Exception as e:
                        print(e)
                        pass

                scraped_news.extend(articles)
                return articles
        except Exception as e:
            print(f'{self.url}/en/bundesliga is not working')
            failed_scrapers.append({'url': self.url, 'error': str(e)})
            pass
