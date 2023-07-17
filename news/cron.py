from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from news.models import News, Website
import asyncio
from news.utils import fetch_news_async, get_all_scrapers


def fetch_news():
    print('started scraping')
    scrapers = list(Website.objects.all())
    
    scraped_news = []

    asyncio.run(fetch_news_async(scrapers, scraped_news, True))

    news_before_db = [News(title=news['title'], url=news['url'],
                           img=news['img'], website=news['website']) for news in scraped_news]

    # try:
    News.objects.bulk_create(news_before_db, ignore_conflicts=True)

    print(len(news_before_db))

    return True


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_news, 'interval', minutes=240)  # every four hours
    scheduler.start()


# fetch_news()
