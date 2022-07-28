from .models import News, Interest
from .utils import get_all_scrapers, fetch_news_async
from django_cron import CronJobBase, Schedule
import asyncio
import random

class ScrapersCronJob(CronJobBase):
    RUN_EVERY_MINS = 120 # every two hours
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'my_app.my_cron_job' # unique code to identify the particular cron task

    def run_all_scrapers(self):

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
    
    
class ScrapersCronJob2(CronJobBase):
    # RUN_EVERY_MINS = 120 # every two hours
    RUN_EVERY_MINS = 1 # every minute
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'my_app.my_cron_job' # unique code to identify the particular cron task

    def run_all_scrapers(self):
        print('running this cron job oo')