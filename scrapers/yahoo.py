from bs4 import BeautifulSoup 
import requests

response_text= requests.get('https://www.theguardian.com/uk/technology').text

content= BeautifulSoup(response_text, 'html.parser')
news_section= content.find_all('div', {'class':'fc-item__container'})

print(result)


class TheGuardianScraper:
    '''
    category=[international
            ,UK
            ,Coronavirus
            ,Climate crisis
            ,Environment
            ,Science
            ,Global development
            ,Football
            ,Tech
            ,Business
            ,Obituaries]
    '''
    def __init__(self, category='international') :
        self.title='The Guardian'
        self.favicon_url= 'https://www.theguardian.com/favicon.ico'
        sites=['international'
            ,'uk'
            ,Coronavirus
            ,Climate crisis
            ,Environment
            ,Science
            ,Global development
            ,Football
            ,Tech
            ,Business
            ,Obituaries]
        content= BeautifulSoup(response_text, 'html.parser')
        news_section= content.find_all('div', {'class':'fc-item__container'})
    
    def scrape(self):
        result=[{
                'title': i.find('h3', {'class':'fc-item__title'}).text.strip(), 
                'url':i.find('h3', {'class':'fc-item__title'}).find('a')['href'], #fix
                'img':i.find('img')['src'], 
                'metadata': {'website': self.title, 'favicon': self.favicon_url}
                } for i in news_section if i.find('img') != None]
        return result
