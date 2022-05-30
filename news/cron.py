from .models import News, Interest
from .utils import get_all_scrapers, fetch_news_async
import asyncio
import random


def run_all_scrapers():
    print('running all the scrapers')
    scrapers = get_all_scrapers()
    scraped_news = []

    # get news using all the scrapers we have
    scraped_news = asyncio.run(fetch_news_async(scrapers, scraped_news))

    # save the news to the database
    for news in scraped_news:
        try:
            news = News.objects.get_or_create(
                title=news['title'], url=news['url'], img=news['img'])
        except Exception as e:
            print(e)
            print(news)
            print(
                f"Error while adding news to database. Skipping... {news['title']}")
            pass

    return True