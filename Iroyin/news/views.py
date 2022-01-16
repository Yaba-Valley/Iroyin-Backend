import json
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, Http404
from .scraper import PunchScraper
import json
from .models import News, User

# Create your views here.

def index(request):
    
    try:
        
        me = User.objects.get(username = 'jeremiah')
        
        punchScraper = PunchScraper('politics')
        
        
        data = punchScraper.scrape()
                
        newsSeen = [news.serialize() for news in me.newsSeen.all()]
        newsInteracted = [news.serialize() for news in me.newsIntereactedWith.all()]
    
        ids, titles, urls,interactions=[],[],[],[]
        
        for i in range(len(newsSeen)):
            #print(newsSeen[i])
            ids.append(newsSeen[i]['newsId'])
            titles.append(newsSeen[i]['title'])
            urls.append(newsSeen[i]['url'])
            
            if newsSeen[i] in newsInteracted:
                interactions.append(1)
            else:
                interactions.append(0)
        
        trainingData = {'ids': ids, 'titles': titles, 'urls': urls, 'interactions': interactions}
        print('trainging data:', trainingData)
        
        # data = model.predict(trainingData, dataFromScraper)
        
        for news in data:
            try:
                existing_news = get_object_or_404(News, url = news['url'])
                me.newsSeen.add(existing_news)
            except Http404:
                me.newsSeen.add(News.objects.create(title = news['headline'], url = news['url']))
                
        me.save()
            
        
    except Exception as e:
        print(e)
        pass
        
    
    return JsonResponse(json.dumps(data), safe=False)


def prepareDataForModel(user):
    newsSeen = list(user.newsSeen.all())
    newInteractedWith = list(user.newsIntereactedWith.all())

    # for news in newsSeen:
        # if(+)