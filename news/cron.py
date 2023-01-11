from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from news.models import News
import asyncio
from news.utils import fetch_news_async, get_all_scrapers


def fetch_news():
    print('started scraping')
    scrapers = get_all_scrapers()

    scraped_news = []

    asyncio.run(fetch_news_async(scrapers, scraped_news))

    news_before_db = [News(title=news['title'], url=news['url'], img=news['img'], website_name=news['metadata']
                           ['website'], website_favicon=news['metadata']['favicon']) for news in scraped_news]
    
    # try:
    News.objects.bulk_create(news_before_db, ignore_conflicts=True)
    # except Exception as e:
        # pass

    return True


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_news, 'interval', minutes=240)  # every four hours
    scheduler.start()