from bs4 import BeautifulSoup 
import requests

r= requests.get('https://news.yahoo.com/world/')

class Scraper:
    def __init__(self, scraper_name):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Cookie': 'tnw_morph=973357127; tfv=2022-09-29T18:52:23.395+01:00; gdpr-auditId=fad5b09eed7c4dfb855caaaaa25eb995; __gads=ID=358254a7976f22ff:T=1664473946:S=ALNI_MZNOlKY6jdXhmMEFheTmuSSWNQRtg; __gpi=UID=00000af0d6b42650:T=1664473946:RT=1664473946:S=ALNI_MYHrIOXf1xBZo_gtbQmLFrsy_z5rQ; __hstc=111399067.cc4094bf9ee50368559c2ffc942bc67e.1664473954009.1664473954009.1664473954009.1; hubspotutk=cc4094bf9ee50368559c2ffc942bc67e; tlv=2022-09-29T18:56:02.713+01:00; _ga=GA1.1.1246751966.1664473946; _ga_1FX48DMMCB=GS1.1.1664473947.1.1.1664475231.0.0.0'
        }
        self.name = scraper_name

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