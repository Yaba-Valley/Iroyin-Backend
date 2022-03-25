import asyncio
import aiohttp
import time
import math
from functools import wraps
from asyncio.proactor_events import _ProactorBasePipeTransport
from news.scraper.interest_scraper import INTEREST_TO_SCRAPER_MAP


def prepareDataForModel(data, newsInteracted):

    titles, urls, interactions, imgs, meta = [], [], [], [], []

    for i in range(len(data)):
        print(
            f"TITLE: {data[i]['title']} IMAGE: {data[i]['img']}")

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
        return {'titles': titles, 'urls': urls, 'interactions': interactions, 'imgs': imgs, 'meta': meta}

    return {'titles': titles, 'urls': urls, 'imgs': imgs, 'meta': meta}


def silence_event_loop_closed(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except RuntimeError as e:
            if str(e) != 'Event loop is closed':
                raise
    return wrapper


_ProactorBasePipeTransport.__del__ = silence_event_loop_closed(
    _ProactorBasePipeTransport.__del__)


async def fetch_news_async(scrapers, news=[]):

    start_time = time.time()
    tasks = []

    async with aiohttp.ClientSession() as session:
        for scraper in scrapers:
            task = asyncio.create_task(scraper.scrape(session, news))
            tasks.append(task)

        await asyncio.gather(*tasks)
        print('TIME TAKEN:', math.floor(time.time() - start_time), 's')

        return news


def get_scrapers_based_on_user_interest(user):

    scrapers = []
    user_interests = [interest.name.upper()
                      for interest in user.interests.all()]

    for interest in user_interests:
        scrapers.extend(INTEREST_TO_SCRAPER_MAP[interest])

    return scrapers
