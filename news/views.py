import asyncio
import json
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt

from news.scraper.sports import BundesligaScraper, GoalDotComScraper, SkySportScraper
from .scraper import EPLScraper, LaLigaScraper, PunchScraper
import json
from .models import News, User
from .recommend import Machine
from .utils import fetch_news_async, prepareDataForModel


def index(request):
    
    try: 
        me = User.objects.get(username = 'jeremiah')
        
        data = []
        
        scrapers = [
            PunchScraper(topic = 'sports'),
            GoalDotComScraper(),
            SkySportScraper(),
            EPLScraper(),
            LaLigaScraper(),
            BundesligaScraper()
        ]
        
        data = asyncio.run(fetch_news_async(scrapers, data))
        
        data_to_predict_with = prepareDataForModel(data = data, newsInteracted=None)
        
        recommend_news=Machine(1).recommend(data_to_predict_with)
        
        for i in range(len(recommend_news['titles'])):
            try:
                existing_news = get_object_or_404(News, url = recommend_news['urls'][i])
                me.newsSeen.add(existing_news)
            except Http404:
                me.newsSeen.add(News.objects.create(title = recommend_news['titles'][i], url = recommend_news['urls'][i]))
                
        me.save()
        
        news_for_frontend = []
        # restructure news for FE
        for i in range(len(recommend_news['titles'])):
            news_for_frontend.append({'title': recommend_news['titles'][i], 'url': recommend_news['urls'][i], 'img': recommend_news['imgs'][i]})
                                          
        return JsonResponse({'news': news_for_frontend})
            
    except Exception as e:
        print(e)
        return HttpResponse(f'<h1>THere is an error <hr /> {e}</h1>')


@csrf_exempt
def indicate_interaction(request):
    
    request_body_unicode = request.body.decode('utf-8')
    request_body = json.loads(request_body_unicode)
    news_url = request_body['news_url']
    
    try:
        active_user = get_object_or_404(User, username = 'jeremiah')
        current_news = get_object_or_404(News, url = news_url)   
        active_user.newInteractedWith.add(current_news)
    except Http404:
        return JsonResponse({'message': f'News with url {news_url} does not exist', 'success': False})
    return JsonResponse({'message': 'Interaction has been recorded', 'success': True})
    
    
    
def login(request):
    email = request.POST.get('email_address')
    password = request.POST.get('password')
    

def register(request):
    pass
