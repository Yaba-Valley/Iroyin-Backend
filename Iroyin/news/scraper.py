from cmath import e
from bs4 import BeautifulSoup
import requests
#import cfscrape


def main ():
    pass

class PunchScraper:
    def __init__(self, topic) -> None:
        self.url = f'https://punchng.com/topics/{topic}/'

    def scrape(self):

        request = requests.get(self.url)
        soup = BeautifulSoup(request.text, 'html.parser')
        
        value = soup.find_all('article', {'class': 'entry-item-simple'})
        headlines=[]
        
        for i in value:
            try:
                img=i.find('img').get('src')
                news=i.find('h3', {'class': 'entry-title'}).text
                link= i.find('h3', {'class': 'entry-title'}).find('a')['href']
                headlines.append({'title':news, 'url':link, 'img':img})
            except:
                pass
        
        return headlines

class VanguardScraper:
    def __init__(self, topic) -> None:
        self.url = f'https://www.vanguardngr.com/category/{topic}/'

    def scrape(self):

        # get big thumbnail news
        request = requests.get(self.url).content
        soup = BeautifulSoup(request, 'lxml')
        value = soup.find_all('h2', {'class': 'entry-title'})

        print(soup)

        headlines = [{'title': i.text, 'url': i.find('a')['href']} for i in value]

        return headlines


class GoalDotComScraper:
    def __init__(self) -> None:
        self.url = 'https://www.goal.com/en-ng/news/1'

    def scrape(self):

        request = requests.get(self.url)
        soup = BeautifulSoup(request.text, 'html.parser')
        value=soup.find_all('tr')
        headlines=[]


        for i in value:
            try:
                img=i.find('img').get('src')
                news=i.find('h3',{'class':'widget-news-card__title'})['title']
                link= self.url+i.find('a')['href']
                headlines.append({'title':news, 'url':link, 'img':img})
            except Exception as e:
                pass
        



        return headlines


print(GoalDotComScraper().scrape())

class SkySportScraper:
    def __init__(self) -> None:
        # the breaking news section of goal dot com (nigeria version)
        self.url = 'https://www.skysports.com/news-wire'

    def scrape(self):

        request = requests.get(self.url)
        soup = BeautifulSoup(request.text, 'html.parser')
        news=soup.find_all('a', {'class':'news-list__headline-link'})

        headlines = [{'title': article.text.strip(), 'url': article['href']} for article in news]



        return headlines

class EPLScraper:
    def __init__(self) -> None:
        # the breaking news section of goal dot com (nigeria version)
        self.url = 'https://www.premierleague.com'

    def scrape(self):

        request = requests.get(self.url+'/news')
        soup = BeautifulSoup(request.text, 'html.parser')
        news=soup.find_all('a', {'class':'thumbnail thumbLong'})


        headlines = [{'title': article.find('span', {'class':'title'}).text, 'url': self.url+article['href']} for article in news]



        return headlines


class LaLigaScraper:
    def __init__(self) -> None:
        # the breaking news section of goal dot com (nigeria version)
        self.url = 'https://www.laliga.com/en-ES/news'

    def scrape(self):

        request = requests.get(self.url, verify=False)
        soup = BeautifulSoup(request.text, 'html.parser')
        news=soup.find_all('div', {'class':'styled__NewInfoContainer-sc-9rnm90-0'})

        headlines = [{'title': article.find('h3', {'class':'styled__TextHeaderStyled-sc-1edycnf-0'}).text, 'url': article.find('a')['href']} for 
article in news]

        return headlines


class BundesligaScraper:
    def __init__(self) -> None:
        self.url = 'https://www.bundesliga.com/en/bundesliga'


    def scrape(self):
        request = requests.get(self.url)
        soup = BeautifulSoup(request.text, 'html.parser')
        news = soup.find_all('')

        return soup
