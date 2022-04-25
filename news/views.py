import asyncio
import json
from re import template
from django.db import IntegrityError
from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.contrib.auth.password_validation import validate_password
from django.template.loader import render_to_string


from .models import Interest, News, User
from .recommend import Machine
from .utils import fetch_news_async, prepareDataForModel, get_scrapers_based_on_user_interest, send_email


def index(request):

    try:
        me = User.objects.get(email='jeremiahlena13@gmail.com')
        print(me)

        data = []

        scrapers = get_scrapers_based_on_user_interest(me)

        data = asyncio.run(fetch_news_async(scrapers, data))

        data_to_predict_with = prepareDataForModel(
            data=data, newsInteracted=None)

        recommend_news = Machine(1).recommend(data_to_predict_with)

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

        request_body = json.loads(request.body.decode('utf-8'))
        email = request_body['email']
        password = request_body['password']

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
        return JsonResponse({'success': False, 'errors': [], 'message': "Request Not Allowed"}, status=405)


@csrf_exempt
def register(request):

    if request.method == "POST":

        request_body = json.loads(request.body.decode('utf-8'))
        email = request_body['email'].strip()
        full_name = request_body['fullName'].strip().split(' ')
        password = request_body['password'].strip()

        if len(full_name) == 1:
            if full_name[0] == '':
                full_name = False
            else:
                first_name = full_name[0]
                last_name = ''
        else:
            first_name = full_name[0]
            last_name = full_name[len(full_name) - 1]

            full_name = True

        if full_name and email and password:
            try:

                # try to get the user to know if a user already exists with the email address
                user = User.objects.filter(email=email)

                if len(user) == 1:
                    raise IntegrityError()

                # this code only runs if there no user with the same email address

                test_user = User(
                    email=email, first_name=first_name, last_name=last_name)

                validate_password(password=password, user=test_user)

                test_user.set_password(password)

                test_user.save()
                
                
                #SENDING ACTIVATION MAIL
                template_string = render_to_string('welcomeAndActivateAccount.html', { 'registered_user': test_user })
                
                res = send_email('Heeyyyy, We\'re sooo happy to have you here😊🎉🎉', template_string, email, f"{first_name} {last_name}")
                
                print('email sending res', res)


                return JsonResponse({
                    'success': True,
                    'message': 'Account has been created successfully. Check your mail to activate your account',
                    'data': {
                        'email': email,
                    }
                }, status=200)

            except ValidationError as errors:
                validation_errors = []

                [validation_errors.append(str(error)) for error in errors]

                return JsonResponse({'success': False, 'message': 'Please review your password', 'errors': validation_errors}, status=400)
            except IntegrityError:
                return JsonResponse({'success': False, 'message': 'Email Address is already in use', 'errors': ['Email Already in Use']}, status=400)

        else:
            errors = []

            if not email:
                errors.append('Email cannot be empty')

            if not password:
                errors.append('Password cannot be empty')

            if not full_name:
                errors.append('Your fullname cannot be empty')

            return JsonResponse({'success': False, 'message': 'Please fill the required fields', 'errors': errors}, status=400)

    else:
        return JsonResponse({'success': False, 'message': "Request Not Allowed"}, status=405)


@csrf_exempt
def activate_account(request):
    
    user = User.objects.get(email = 'jeremiahlena13@gmail.com')
    
    template_string = render_to_string('welcomeEmail.html', { 'registered_user': user })
    res = send_email('Heeyyyy, We\'re sooo happy to have you here😊🎉🎉', template_string, user.email, user.first_name)
    
    return JsonResponse({'message': 'tried seending mail'}, status = res.status_code)


def get_all_interests(request):
    try:
        interest_names = [{'name': interest.name, 'id': interest.id}
                          for interest in Interest.objects.all()]
        return JsonResponse({'success': True, 'data': interest_names, 'message': "Successfully retrieved interests"}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'errors': e, 'message': 'An Error Occurred'}, status=500)


@csrf_exempt
def save_interests(request):
    """
    This endpoint takes the id of the interests as an array and saves it to the user's profile
    """

    if request.method == "POST":
        request_body = json.loads(request.body.decode('utf-8'))
        user = User.objects.get(email="jeremiahlena13@gmail.com")

        interest_ids = request_body['interests']

        for id in interest_ids:
            interest = Interest.objects.get(id=id)
            user.interests.add(interest)

        return JsonResponse({'success': True, 'message': 'User interests successfully recorded', 'data': interest_ids}, status=200)

    else:
        return JsonResponse({'success': False, 'errors': 'Request Not Allowed'}, status=405)


@csrf_exempt
def remove_interests(request):
    """
    This endpoint takes the id of the interests as an array and removes them from the user's profile
    """
    
    if request.method == "POST":
        request_body = json.loads(request.body.decode('utf-8'))
        user = User.objects.get(email="jeremiahlena13@gmail.com")

        interest_ids = request_body['interests']

        for id in interest_ids:
            interest = Interest.objects.get(id=id)
            user.interests.remove(interest)

        return JsonResponse({'success': True, 'message': 'Successfully removed interests', 'data': interest_ids}, status=200)

    else:
        return JsonResponse({'success': False, 'errors': 'Request Not Allowed'}, status=405)