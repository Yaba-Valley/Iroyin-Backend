import json
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse, Http404
from .scraper import EPLScraper, GoalDotComScraper, LaLigaScraper, PunchScraper, SkySportScraper
import json
from .models import News, User
from .recommend import Machine
from .utils import prepareDataForModel

# Create your views here.

def index(request):
    
    try:
        
        me = User.objects.get(username = 'jeremiah')
        
        data = []
        
        scrapers = [GoalDotComScraper(), SkySportScraper(),LaLigaScraper(), EPLScraper()]
        
        for scraper in scrapers:
            data.extend(scraper.scrape())
            print(scraper)
            print('is done')
                
        newsSeen = [news.serialize() for news in me.newsSeen.all()]
        
        newsInteracted = [news.serialize() for news in me.newsIntereactedWith.all()]
    
        trainingData = prepareDataForModel(data=newsSeen, newsInteracted=newsInteracted)
        
        data_to_predict_with = prepareDataForModel(data = data, newsInteracted=None)
        
        recommend_news=Machine(trainingData).recommend(data_to_predict_with)
        
        # print(recommend_news)
                
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

def indicate_interaction(request, news_id):
    sample_user = User.objects.get(username = 'jeremiah')
    news = News.objects.get(id = news_id)
    
    
def login(request):
    email = request.POST.get('email_address')
    password = request.POST.get('password')
    

def register(request):
    pass


def test_templates(request):
    return render(request, 'index.html')


def profile(request):
    return render(request, 'profile.html')