import asyncio
import aiohttp
import time
import math
from functools import wraps
from asyncio.proactor_events import _ProactorBasePipeTransport


def prepareDataForModel (data, newsInteracted):
    
    titles, urls,interactions,imgs, meta=[],[],[],[], []
        
    for i in range(len(data)):
        titles.append(data[i]['title'])
        urls.append(data[i]['url'])
        imgs.append(data[i]['img'])
        meta.append(data[i]['metadata'])
        
        if newsInteracted is not None:
            if data[i] in newsInteracted:
                interactions.append(1)
            else:
                interactions.append(0)
        
    if newsInteracted is not None:
        return {'titles': titles, 'urls': urls, 'interactions': interactions, 'imgs': imgs, 'meta':meta}
    
    return {'titles': titles, 'urls': urls, 'imgs': imgs, 'meta':meta}


def silence_event_loop_closed(func):
    @wraps(func)
    
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except RuntimeError as e:
            if str(e) != 'Event loop is closed':
                raise
    return wrapper

_ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)


async def fetch_news_async(scrapers, news = []):
    
    start_time = time.time()
    tasks = []

    async with aiohttp.ClientSession() as session:
        for scraper in scrapers:
            task = asyncio.create_task(scraper.scrape(session, news))
            tasks.append(task)
    
        await asyncio.gather(*tasks)
        print('TIME TAKEN:', math.floor(time.time() - start_time), 's')
        
        return news
    

""" async def scrape_website(session, website):
    print('making request to', website)
    async with session.get(website) as response:
        print('made request to', website)
        html_text = await response.text()
        return html_text[:30]
    
 """
 
 
