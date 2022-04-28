import asyncio
import aiohttp
import time
import math
from functools import wraps
from asyncio.proactor_events import _ProactorBasePipeTransport
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
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


def send_email(subject, body, receipient_email, receipient_fullName):

    import environ
    from mailjet_rest import Client

    env = environ.Env()

    environ.Env.read_env()

    mailjet = Client(auth=(env('MAILJET_API_KEY'),
                     env('MAILJET_SECRET_KEY')), version = 'v3.1')

    data = {
        "Messages": [
            {
                "From": {
                    "Email": "jeremiahlena13@gmail.com",
                    "Name": "The ReadNews Team"
                },
                "To": [
                    {
                        "Email": receipient_email,
                        "Name": receipient_fullName
                    }
                ],
                "Subject": subject,
                "TextPart": subject,
                "HTMLPart": body,
                "CustomID": "AppGettingStartedTest"
            }
        ]
    }


    result = mailjet.send.create(data=data)
    print(receipient_fullName)
    print(f"{subject} return {str(result.status_code)}")
    return result


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.pk) + text_type(timestamp) + text_type(user.is_active))

    def send_account_activation_mail(self, request, user):

        site = get_current_site(request).name
        token = TokenGenerator().make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        template_string = render_to_string('activateAccount.html', {
                                           'user': user, 'uid': uid, 'token': token, 'site': site})

        print(template_string)
        # res = send_email('Confirm your email', template_string,
                #    user.email, f"{user.first_name} {user.last_name}")
    
        # print(res)
        
        # return res.status_code;
        
        return template_string;
