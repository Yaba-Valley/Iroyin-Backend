from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from news.models import News
import asyncio
from news.utils import fetch_news_async, get_all_scrapers
from news.scraper import TheNextWebScraper, TechTrendsAfricaScraper


def fetch_news():
    print('started scraping')
    scrapers = get_all_scrapers()
    
    scraped_news = []

    scraped_news = asyncio.run(fetch_news_async(scrapers, scraped_news))

    for news in scraped_news:
        try:
            News.objects.get_or_create(
                title=news['title'], url=news['url'], img=news['img']
            )
        except Exception as e:
            print(e)
            print(news)
            print(
                f"Error while adding news to database. Skipping {news['title']}...")

            pass

    return True


def start():
    print('setting up scheduler...')
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_news, 'interval', minutes=1)
    scheduler.start()
