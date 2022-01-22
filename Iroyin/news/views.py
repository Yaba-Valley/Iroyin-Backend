import json
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, Http404
from .scraper import PunchScraper
import json
from .models import News, User
from .recommend import Machine

# Create your views here.

def index(request):
    
    try:
        
        me = User.objects.get(username = 'jeremiah')
        
        punchScraper = PunchScraper('sports')      
        
        data = punchScraper.scrape()
                
        newsSeen = [news.serialize() for news in me.newsSeen.all()]
        
        newsInteracted = [news.serialize() for news in me.newsIntereactedWith.all()]
    
        trainingData = prepareDataForModel(data=newsSeen, newsInteracted=newsInteracted)
        
        data_to_predict_with = prepareDataForModel(data = data, newsInteracted=None)
        
        recommend_news=Machine(trainingData).recommend(data_to_predict_with)
        
        print(recommend_news)
                
        for i in range(len(recommend_news['titles'])):
            try:
                existing_news = get_object_or_404(News, url = recommend_news['urls'][i])
                me.newsSeen.add(existing_news)
            except Http404:
                me.newsSeen.add(News.objects.create(title = recommend_news['titles'][i], url = recommend_news['urls'][i]))
                
        me.save()
            
        
    except Exception as e:
        print(e)
        pass
        
    
    return JsonResponse(json.dumps({'SCRAPED': data, 'RECOMMENDED': recommend_news}), safe=False)


def prepareDataForModel (data, newsInteracted):
    
    titles, urls,interactions=[],[],[]
        
    for i in range(len(data)):
        #print(data[i])
        titles.append(data[i]['title'])
        urls.append(data[i]['url'])
        
        if newsInteracted is not None:
            if data[i] in newsInteracted:
                interactions.append(1)
            else:
                interactions.append(0)
        
    if newsInteracted is not None:
        return {'titles': titles, 'urls': urls, 'interactions': interactions}
    
    return {'titles': titles, 'urls': urls }


def test_templates(request):
    return render(request, 'index.html')


def profile(request):
    return render(request, 'profile.html')