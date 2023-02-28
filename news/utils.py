import asyncio
import aiohttp
import math
import time
from functools import wraps
from asyncio.proactor_events import _ProactorBasePipeTransport
from news.scraper.interest_scraper import INTEREST_TO_SCRAPER_MAP
from news.scraper.base import Scraper as BaseScraper
from django.template.loader import render_to_string
from authentication.utils import send_email


default_headers = BaseScraper('default').headers


def prepareDataForModel(data, newsInteracted):

    titles, urls, interactions, imgs, meta = [], [], [], [], []

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


async def fetch_news_async(scrapers, news=[], send_mail=False):

    start_time = time.time()
    tasks = []
    failed_scrapers = []

    async with aiohttp.ClientSession(headers=default_headers) as session:
        for scraper in scrapers:
            task = asyncio.create_task(
                scraper.scrape(session, news, failed_scrapers))
            tasks.append(task)

        await asyncio.gather(*tasks)

        time_taken = math.floor(time.time() - start_time)
        print('TIME TAKEN:', time_taken)

        if send_mail:
            email_text = render_to_string(
                'scraperInfo.html', {'failed_scrapers': failed_scrapers, 'time_taken': time_taken})

            res = send_email(
                f'Scraper Information ({len(scrapers)} ran, {len(failed_scrapers)} failed, {len(scrapers) - len(failed_scrapers)} successful)',
                email_text,
                [
                    {
                        'email': 'jeremiahlena13@gmail.com',
                        'fullName': 'Jeremiah Lena'
                    },
                    {
                        'email': 'ikpeleambroseobinna@gmail.com',
                        'fullName': 'Ikepele Ambrose'
                    },
                    {
                        'email': 'odeogberinoluwadamilola@gmail.com',
                        'fullName': 'Oluwadamilola Odeogberin'
                    }
                ]
            )

            print(res)

        return news


def get_all_scrapers():

    scrapers = []

    for scraper in INTEREST_TO_SCRAPER_MAP.values():
        scrapers.extend(scraper)

    return scrapers


def test_scraper(scraper, send_mail=False):
    news = []
    asyncio.run(fetch_news_async(
        scrapers=[scraper], news=news, send_mail=send_mail))

    return news


def send_notification(device_token, message, data):
    from exponent_server_sdk import PushClient, PushMessage, PushServerError, PushTicketError, DeviceNotRegisteredError
    from requests.exceptions import ConnectionError, HTTPError
    
    response = None

    try:
        response = PushClient().publish(
            PushMessage(to=device_token,
                        body=message,
                        data=data))
        print(response)
    except PushServerError as exc:
        print('push server error', exc)
        exit(0)
    except (ConnectionError, HTTPError) as exc:
        print('http/connection error', exc)
        exit(0)

    try:
        response.validate_response()
    except DeviceNotRegisteredError:
        from authentication.models import User
        
        user = User.objects.get(push_notification_token = device_token)
        user.push_token = ''; user.save()
    except PushTicketError as exc:
        print('push ticket error', exc)
        exit(0)


def unionize_queryset_from_list(list_of_querysets):
    if len(list_of_querysets) == 0: return
    
    first_queryset = list_of_querysets[0]
    current_queryset = first_queryset
    
    for i in range(1, len(list_of_querysets)):
        current_queryset = current_queryset.union(list_of_querysets[i])
    
    return current_queryset


def intersect_queryset_from_list(list_of_querysets, model):
    if len(list_of_querysets) == 0: return
    
    first_queryset = list_of_querysets[0]
    current_id_values = set(first_queryset.values_list('id', flat = True))
    
    for i in range(1, len(list_of_querysets)):
        ith_id_values = set(list_of_querysets[i].values_list('id', flat = True))
        current_id_values.intersection_update(ith_id_values)
        
    
    interesected_queryset = model.objects.filter(id__in = current_id_values)
        
    return interesected_queryset
    