import json
import requests
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Interest, News
from .recommend import Machine
from news.scraper.tech import TechCrunchScraper, GlassDoorScraper
from news.scraper.sports import GoalDotComScraper, SkySportScraper, EPLScraper
from news.scraper.fashion import PeopleScraper
from news.scraper.health import VeryWellMindScraper


class GetNews(APIView):

    # permission_classes = (IsAuthenticated, )

    def get(self, request):
        # print(list(request.headers.keys()), '\n\n',
        #       list(request.headers.items()), '\n\n', type(request.headers))
        news_per_page = int(request.GET.get('news_per_page'))
        # first value should be 1
        page_number = int(request.GET.get('page_number'))

        print(news_per_page, page_number)

        if page_number < 1:
            page_number = 1  # first value should be 1

        start = (page_number - 1) * news_per_page
        end = start + news_per_page

        try:
            news = News.objects.order_by('-time_added')[start:end]

            # me = request.user

            """
            what should happen here is that the recommender system is called with the id of the user and 
            the number of news to be returned, the model has access to the database and can get the user's 
            news interaction history. After prediction, it should return the news most likely to be liked by the user
            """

            # news = Machine(me.id).recommend(data_to_predict_with)

            news_for_frontend = []

            for n in list(news):
                news_for_frontend.append(n.serialize())
                # me.newsSeen.add(n)

            # me.save()

            # time.sleep(3)

            return JsonResponse({
                'news': news_for_frontend,
                'current_page': page_number,
                'next_page': page_number + 1,
                'per_page': news_per_page,
                'total_pages': round(News.objects.count() / news_per_page)
            })

        except Exception as e:
            print(e)
            return HttpResponse(f'<h1>THere is an error <hr /> {e}</h1>')

    def post(request):
        return


class Search_News(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, _, title):
        try:
            search_news = [news.serialize() for news in News.objects.filter(
                title__contains=title)]

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


def get_all_interests(request):
    try:
        interest_names = [{'name': interest.name, 'id': interest.id}
                          for interest in Interest.objects.all()]
        return JsonResponse({'success': True, 'data': interest_names, 'message': "Successfully retrieved interests"}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'errors': e, 'message': 'An Error Occurred'}, status=500)


class Get_News_Content(APIView):
    def get(self, request):
        url = request.GET.get('url')
        news = News.objects.get(url=url)
        text_content = news.text_content

        if text_content == '':
            if news.website_name == 'TechCrunch':
                text_content = TechCrunchScraper().scrape_news_content(url=url)
            elif news.website_name == 'Goal.com':
                text_content = GoalDotComScraper().scrape_news_content(url=url)
            elif news.website_name == 'People.com':
                text_content = PeopleScraper().scrape_news_content(url=url)
            elif news.website_name == 'GlassDoor':
                text_content = GlassDoorScraper().scrape_news_content(url=url)
            elif news.website_name == 'VeryWellMind':
                text_content = VeryWellMindScraper().scrape_news_content(url=url)
            elif news.website_name == 'Sky Sports':
                text_content = SkySportScraper().scrape_news_content(url=url)
            elif news.website_favicon == 'Premier League':
                text_content = EPLScraper().scrape_news_content(url=url)

        news.read_count += 1
        news.text_content = text_content
        news.save()

        return JsonResponse({'text': text_content, 'status': 200})


class Save_Interests(APIView):

    permission_classes = [IsAuthenticated]
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

    permssion_classes = [IsAuthenticated]

    def get(self, request):
        me = request.user
        interests = [{'name': interest.name, 'id': interest.id}
                     for interest in me.interests.all()]
        return Response({'success': True, 'interests': interests, 'message': 'Successfully retrieved user interest'})
