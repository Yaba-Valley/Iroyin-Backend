import asyncio
import json
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token

from .models import News, User
from .recommend import Machine
from .utils import fetch_news_async, prepareDataForModel, get_scrapers_based_on_user_interest


def index(request):

    try:
        me = User.objects.get(username='jeremiah')

        data = []

        scrapers = get_scrapers_based_on_user_interest(me)

        data = asyncio.run(fetch_news_async(scrapers, data))

        data_to_predict_with = prepareDataForModel(
            data=data, newsInteracted=None)

        recommend_news = Machine(1).recommend(data_to_predict_with)

        print(recommend_news)
        print(data)

        for i in range(len(recommend_news['titles'])):
            try:
                existing_news = get_object_or_404(
                    News, url=recommend_news['urls'][i])
                me.newsSeen.add(existing_news)
            except Http404:
                me.newsSeen.add(News.objects.create(
                    title=recommend_news['titles'][i], url=recommend_news['urls'][i]))

        me.save()

        news_for_frontend = []
        # restructure news for FE
        for i in range(len(recommend_news['titles'])):
            news_for_frontend.append({'title': recommend_news['titles'][i], 'url': recommend_news['urls'][i], 'img': recommend_news['imgs'][i], 'metadata': {
                                      'website': recommend_news['meta'][i]['website'], 'favicon': recommend_news['meta'][i]['favicon']}})

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
        active_user = get_object_or_404(User, username='jeremiah')
        current_news = get_object_or_404(News, url=news_url)
        active_user.newInteractedWith.add(current_news)
    except Http404:
        return JsonResponse({'message': f'News with url {news_url} does not exist', 'success': False})
    return JsonResponse({'message': 'Interaction has been recorded', 'success': True})


@csrf_exempt
def login(request):

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email and password:
            try:
                user = get_object_or_404(User, email=email)

                if user.check_password(password):

                    csrf_token = get_token(request)

                    return JsonResponse(
                        {
                            'message': 'You have successfully logged in',
                            'error': False,
                            'token': csrf_token,
                            'email': user.email
                        }, status=200
                    )
                else:
                    return JsonResponse(
                        {
                            'message': 'Incorrect Login Credentials',
                            'error': True
                        }, status=404
                    )
            except Http404:
                return JsonResponse(
                    {
                        'message': 'Incorrect Login Credentials',
                        'error': True
                    },  status=404
                )
        else:
            return JsonResponse({'error': True, 'message': "Please input required fields"})
    else:
        return JsonResponse({'error': True, 'message': "Request Not Allowed"}, status=400)


def register(request):
    # if
    pass
