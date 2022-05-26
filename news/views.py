import asyncio
import json
import requests
from django.db import IntegrityError
from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.password_validation import validate_password
from django.template.loader import render_to_string
from django.utils.encoding import force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Interest, News, User
from .recommend import Machine
from .utils import fetch_news_async, prepareDataForModel, get_scrapers_based_on_user_interest, send_email, TokenGenerator


class GetNews(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request):

        try:
            data = []
            me = request.user

            scrapers = get_scrapers_based_on_user_interest(me)

            data = asyncio.run(fetch_news_async(scrapers, data))

            data_to_predict_with = prepareDataForModel(
                data=data, newsInteracted=None)

            recommend_news = Machine(1).recommend(data_to_predict_with)

            news_for_frontend = list(recommend_news.values())

            for i in range(len(news_for_frontend)):
                try:
                    #restructure the news recommend for the frontend
                    #news_for_frontend.append({'title': recommend_news['titles'][i], 'url': recommend_news['urls'][i], 'img': recommend_news['imgs'][i], 'metadata': {
                    #'website': recommend_news['meta'][i]['website'], 'favicon': recommend_news['meta'][i]['favicon']}})
                    
                    # check to see if news exists with this url
                    existing_news = get_object_or_404(
                        News, url=news_for_frontend[i]['titles']['urls'])
                    
                    # add the news to the user's seen news if it already exists
                    me.newsSeen.add(existing_news)
                
                except Http404:
                    
                    # create a new News object and addit to the user's seen news
                    me.newsSeen.add(News.objects.create(
                        title=news_for_frontend[i]['titles'], url=recommend_news[i]['urls']))

            me.save()

            return JsonResponse({'news': news_for_frontend})

        except Exception as e:
            print(e)
            return HttpResponse(f'<h1>THere is an error <hr /> {e}</h1>')

class Search_News(APIView):
    
    permission_classes = [ IsAuthenticated ]
    
    def get(self, request, title):
        try:
            search_news = News.objects.filter(title__contains = title).values_list('title', flat = True)
            
            return Response({'res': list(search_news)})
        except News.DoesNotExist:
            return Response({'res': 404})
        


class Indicate_Interaction(APIView):
    
    def post(self, request):
        request_body_unicode = request.body.decode('utf-8')
        request_body = json.loads(request_body_unicode)
        news_url = request_body['news_url']

        try:
            active_user = request.user
            current_news = get_object_or_404(News, url=news_url)
            active_user.newInteractedWith.add(current_news)
        except Http404:
            return JsonResponse({'message': f'News with url {news_url} does not exist', 'success': False})
        return JsonResponse({'message': 'Interaction has been recorded', 'success': True})


@csrf_exempt
def login(request):

    if request.method == "POST":

        request_body = json.loads(request.body.decode('utf-8'))
        email = request_body['email'].strip()
        password = request_body['password'].strip()

        if email and password:
            try:
                user = get_object_or_404(User, email=email)

                if user.check_password(password):

                    # generate a token
                    site = get_current_site(request).__str__()
                    res = requests.post(
                        f"http://{site}/api/token/", {'email': email, 'password': password})

                    # if the token was generated successfully
                    if res.status_code == 200:
                        token_response = res.json()
                        return JsonResponse(
                            {
                                'message': 'You have successfully logged in',
                                'success': True,
                                'data': {
                                    'token': token_response['access'],
                                    'email': user.email,
                                    'first_name': user.first_name,
                                    'last_name': user.last_name
                                }
                            }, status=200
                        )
                    else:

                        html_string = TokenGenerator().send_account_activation_mail(request, user)

                        # failure to generate token is mostly a result of user not been activated
                        return JsonResponse(
                            {
                                'success': False,
                                'message': 'Your account has not been activated',
                                'errors': []
                            }
                        )

                        # return HttpResponse(html_string)

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

                # SENDING ACTIVATION MAIL
                template_string = render_to_string('welcomeEmail.html', {
                                                   'registered_user': test_user})

                welcome_mail_res = send_email('Heeyyyy, We\'re sooo happy to have you here😊🎉🎉',
                                 template_string, email, f"{first_name} {last_name}")

                activation_mail_res = TokenGenerator().send_account_activation_mail(request, test_user)
                
                
                print(welcome_mail_res, activation_mail_res)

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


class Activate_Account(APIView):
    
    def get(self, request,  uid, token):
        
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user_id = int(user_id)

            user = User.objects.get(id=user_id)

            is_valid_token = TokenGenerator().check_token(user=user, token=token)

            if is_valid_token:
                print('Token is Valid')
                user.is_active = True
                user.save()
            else:
                return HttpResponse('Invalid token')

            return HttpResponse('hi ' + user.first_name + '. You can now log in normally')

        except User.DoesNotExist:
            return HttpResponse("Guy how far, this person no dey our databse")
        except DjangoUnicodeDecodeError:
            return HttpResponse('I catch you, couldn\'t decode this unicode')

    # user = User.objects.get(email='jeremiahlena13@gmail.com')

    # template_string = render_to_string(
        # 'welcomeEmail.html', {'registered_user': user})
    # res = send_email('Heeyyyy, We\'re sooo happy to have you here😊🎉🎉',
        #  template_string, user.email, user.first_name)

    # return JsonResponse({'message': 'tried seending mail'}, status=res.status_code)


def get_all_interests(request):
    try:
        interest_names = [{'name': interest.name, 'id': interest.id}
                          for interest in Interest.objects.all()]
        return JsonResponse({'success': True, 'data': interest_names, 'message': "Successfully retrieved interests"}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'errors': e, 'message': 'An Error Occurred'}, status=500)


class Save_Interests(APIView):
    """
    This endpoint takes the id of the interests as an array and saves it to the user's profile
    """
    
    def post(self, request):
        request_body = json.loads(request.body.decode('utf-8'))
        user = request.user

        interest_ids = request_body['interests']

        for id in interest_ids:
            interest = Interest.objects.get(id=id)
            user.interests.add(interest)

        return JsonResponse({'success': True, 'message': 'User interests successfully recorded', 'data': interest_ids}, status=200)


    def get(self, request):
        return JsonResponse({'success': False, 'errors': 'Request Not Allowed'}, status=405)



class Remove_Interests(APIView):
    """
    This endpoint takes the id of the interests as an array and removes them from the user's profile
    """

    def post(self, request):
        request_body = json.loads(request.body.decode('utf-8'))
        user = request.user

        interest_ids = request_body['interests']

        for id in interest_ids:
            interest = Interest.objects.get(id=id)
            user.interests.remove(interest)

        return JsonResponse({'success': True, 'message': 'Successfully removed interests', 'data': interest_ids}, status=200)


    def get(self, request):
        return JsonResponse({'success': False, 'errors': 'Request Not Allowed'}, status=405)


class UserInterests(APIView):

    permssion_classes = [ IsAuthenticated ]
        
    def get(self, request):
        me = request.user
        interests = [ {'name': interest.name, 'id': interest.id } for interest in me.interests.all() ]
        return Response({'success': True, 'interests': interests, 'message': 'Successfully retrieved user interest'})
        
        

class HelloView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        content = {'message': 'Hello, GeeksforGeeks',
                   'username': request.user.email}
        return Response(content)
