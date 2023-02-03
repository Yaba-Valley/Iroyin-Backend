import json
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Interest, News
from .recommend import Machine
from news.scraper.tech import TechCrunchScraper, GlassDoorScraper, TheNextWebScraper, TechTrendsAfricaScraper, FreeCodeCampScraper
from news.scraper.sports import GoalDotComScraper, SkySportScraper, EPLScraper
from news.scraper.fashion import PeopleScraper
from news.scraper.health import VeryWellMindScraper


class Get_News(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        news_per_page = int(request.GET.get('news_per_page'))
        # first value should be 1
        page_number = int(request.GET.get('page_number'))

        try:
            recommended = Machine(request.user.id, news_per_page)
            news_for_frontend = []

            for news in recommended:
                news_for_frontend.append({'title': news['title'], 'url': news['url'], 'img': news['img'], 'metadata': {
                                         'website': news['website_name'], 'favicon': news['website_favicon']}})

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


class Search_News(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        title = request.GET.get('title')

        if (title == ''):
            return Response({'res': []}, status=200)
        else:
            try:
                title_qs = News.objects.filter(title__icontains=title)
                website_name_qs = News.objects.filter(
                    website_name__icontains=title)
                union_qs = title_qs.union(website_name_qs)[0:10]

                search_news = [news.serialize() for news in union_qs]

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


class Get_All_Interests(APIView):

    permission_classes = [IsAuthenticated]

    """ 
    This endpoints returns the list of all the interests
    """

    def get(self, request):

        print(request.user)
        try:
            interest_names = [{'name': interest.name, 'id': interest.id}
                              for interest in Interest.objects.all()]
            return JsonResponse({'success': True, 'data': interest_names, 'message': "Successfully retrieved interests"}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'errors': e, 'message': 'An Error Occurred'}, status=500)

    def post(self, request):
        return JsonResponse({'success': False, 'errors': 'Request Not Allowed'}, status=405)


class Get_News_Content(APIView):
    def get(self, request):
        url = request.GET.get('url')
        news = News.objects.get(url=url)
        text_content = news.text_content

        if text_content == '' or text_content == 'None':
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
            elif news.website_name == 'Premier League':
                text_content = EPLScraper().scrape_news_content(url=url)
            elif news.website_name == 'The Next Web':
                text_content = TheNextWebScraper().scrape_news_content(url=url)
            elif news.website_name == 'Tech Trends Africa':
                text_content = TechTrendsAfricaScraper().scrape_news_content(url=url)
            elif news.website_name == 'FreeCodeCamp':
                text_content = FreeCodeCampScraper().scrape_news_content(url=url)

        news.read_count += 1
        if not text_content == 'None':
            news.text_content = text_content
            news.save()

            return JsonResponse({'text': text_content, 'status': 200})
        else:
            return JsonResponse({'text': None, 'status': 400, 'message': 'Unable to retrieve web content'}, status=400)


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

    permission_classes = [IsAuthenticated]
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


class Redirect_To_App(APIView):
    def get(self, request):
        news_url = request.GET.get('url')
        route = request.GET.get('route')
        news = News.objects.get(url=news_url)
        host = request.GET.get('host')
        
        expo_url = f'{host}{route}?title={news.title}&url={news.url}&img={news.img}&favicon={news.website_favicon}&website={news.website_name}'

        return render(request, 'redirect_to_app.html', {'redirect_url': expo_url})
