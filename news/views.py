import asyncio
import json
from django.db import IntegrityError
from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.contrib.auth.password_validation import validate_password

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
                            'success': True,
                            'data': {
                                'token': csrf_token,
                                'email': user.email
                            }
                        }, status=200
                    )
                else:
                    return JsonResponse(
                        {
                            'message': 'Incorrect Login Credentials',
                            'success': False,
                            'errors': [],
                        }, status=404
                    )
            except Http404:
                return JsonResponse(
                    {
                        'message': 'Incorrect Login Credentials',
                        'success': False,
                        'errors': []
                    },  status=404
                )
        else:
            return JsonResponse({'success': False, 'errors': [],  'message': "Please input required fields"}, status=400)
    else:
        return JsonResponse({'success': False, 'errors': [], 'message': "Request Not Allowed"}, status=400)


@csrf_exempt
def register(request):

    if request.method == "POST":
        email = request.POST['email']
        full_name = request.POST['fullName'].split(' ')
        password = request.POST['password']

        first_name = full_name[0]
        last_name = full_name[1]

        if full_name and email and password:
            try:
                
                # try to get the user to know if a user already exists with the email address
                user = User.objects.filter(email = email);
                
                if len(user) == 1:
                    raise IntegrityError()
                
                
                # this code only runs if there no user with the same email address
                
                test_user = User(email=email, first_name=first_name, last_name=last_name)
                
                validate_password(password=password, user=test_user)

                test_user.set_password(password)

                test_user.save()

                """
                A MAIL IS SENT TO THE USER ADDRESS IN ORDER TO ACTIVATE HIS ACCOUNT
                """

                return JsonResponse({
                    'success': True,
                    'message': 'Account has been created successfully. Check your mail to activate your account',
                    'data': {
                        'email': email,
                    }
                }, status=200)

            except ValidationError as errors:
                validation_errors = []
                
                [ validation_errors.append(str(error)) for error in errors ]
                
                return JsonResponse({'success': False, 'message': 'Please review your password', 'errors': validation_errors}, status=400)
            except IntegrityError:
                return JsonResponse({'success': False, 'message': 'Email Address is already in use', 'errors': ['Email Already in Use']}, status=400)

    else:
        return JsonResponse({'success': False, 'message': "Request Not Allowed"}, status=400)
