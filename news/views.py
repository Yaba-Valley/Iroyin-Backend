import json
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Interest, News
from .recommend import Machine
from .screenshot import get_image
from news.scraper.tech import TechCrunchScraper, GlassDoorScraper, TheNextWebScraper, TechTrendsAfricaScraper, FreeCodeCampScraper
from news.scraper.sports import GoalDotComScraper, SkySportScraper, EPLScraper
from news.scraper.fashion import PeopleScraper, GlamourScraper
from news.scraper.health import VeryWellMindScraper, VeryWellFamilyScraper, VeryWellFitScraper, VeryWellHealthScraper
from news.scraper.finance import FinanceSamuraiScraper, InvestopediaScraper, ForbesScraper
from authentication.models import User
from news.utils import intersect_queryset_from_list
import urllib


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
                                         'website': news['website_name'], 'favicon': news['website_favicon'], 'time_added': news['time_added']}})

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
                all_words_queryset = []

                for word in title.split(' '):
                    if len(word) == 1:
                        continue
                    elif len(word) <= 3:
                        all_words_queryset.append(
                            News.objects.filter(title__icontains=f" {word}").union(
                                News.objects.filter(title__icontains=f"{word} ")).union(
                                News.objects.filter(title__icontains=f"\'{word}")).union(
                                News.objects.filter(title__icontains=f"{word}\'")).union(
                                News.objects.filter(title__icontains=f"\"{word}")).union(
                                News.objects.filter(title__icontains=f"{word}\"")).union(
                                News.objects.filter(title__icontains=f"‘{word}")).union(
                                News.objects.filter(title__icontains=f"{word}’"))
                        )
                    else:
                        all_words_queryset.append(
                            News.objects.filter(title__icontains=word))

                contains_all_words_queryset = intersect_queryset_from_list(
                    all_words_queryset, News).union(News.objects.filter(website_name__icontains=title)).order_by('-time_added')

                search_news = [news.serialize()
                               for news in contains_all_words_queryset]

                return Response({'res': list(search_news)})
            except News.DoesNotExist:
                return Response({'res': 404})


class Indicate_Interaction(APIView):

    def post(self, request):
        request_body_unicode = request.body.decode('utf-8')
        request_body = json.loads(request_body_unicode)
        news_url = request_body['news_url']
        effect = request_body['effect']

        """ 
        the `effect` field is either "POSITIVE" or "NEGATIVE", 
        positive is when the the effect is going to increase the value of the database, eg, liking or saving a news
        negative is when the effect is going to decrease the value in the database eg, dislking a news or removing a saved news
        
        
        the `action` field is either of the following: READ, LIKE, SAVE, SHARE, DISLIKE
        """

        action = request_body['action']

        try:
            active_user = User.objects.get(id=request.user.id)
            print(active_user, request.user)
            current_news = get_object_or_404(News, url=news_url)

            if action.upper() == 'SHARE':
                if effect == 'POSITIVE':
                    active_user.shared_news.add(current_news)
                else:
                    active_user.shared_news.remove(current_news)
            elif action.upper() == 'LIKE':
                if effect == "POSITIVE":
                    active_user.liked_news.add(current_news)
                else:
                    active_user.liked_news.remove(current_news)
            elif action.upper() == 'SAVE':
                if effect == "POSITIVE":
                    active_user.saved_news.add(current_news)
                else:
                    active_user.saved_news.remove(current_news)
            elif action.upper() == 'READ':
                active_user.newInteractedWith.add(current_news)
            elif action.upper() == 'DISLIKE':
                # remove any relationship between the news and the user
                try:
                    active_user.shared_news.remove(current_news)
                    active_user.liked_news.remove(current_news)
                    active_user.saved_news.remove(current_news)
                    active_user.newInteractedWith.remove(current_news)
                except News.DoesNotExist:
                    print('news does not exist')

                # the only relationship that should exist is the negative relationship of dislike
                active_user.disliked_news.add(current_news)
            else:
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


class Get_News_Details(APIView):
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
            elif news.website_favicon == 'VeryWellHealth':
                text_content = VeryWellHealthScraper().scrape_news_content(url=url)
            elif news.website_name == 'VeryWellFit':
                text_content = VeryWellFitScraper().scrape_news_content(url=url)
            elif news.website_name == 'VeryWellFamily':
                text_content = VeryWellFamilyScraper().scrape_news_content(url=url)
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
            elif news.website_name == 'FinanceSamurai':
                text_content = FinanceSamuraiScraper().scrape_news_content(url=url)
            elif news.website_name == 'Investopedia':
                text_content = InvestopediaScraper().scrape_news_content(url=url)
            elif news.website_name == 'Glamour':
                text_content = GlamourScraper().scrape_news_content(url=url)
            elif news.website_name == 'Forbes':
                text_content = ForbesScraper().scrape_news_content(url=url)

        news.read_count += 1
        if not text_content == 'None':
            news.text_content = text_content
            news.save()

            return JsonResponse({'title': news.title, 'url': news.url, 'img': news.img, 'metadata': {
                'website': news.website_name, 'favicon': news.website_favicon}, 'text_content': text_content, 'is_saved': request.user.saved_news.contains(news), 'is_liked': request.user.liked_news.contains(news), 'status': 200})
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
        host = request.GET.get('host')

        news = News.objects.get(url=news_url)
        safe = "~()*!.'"

        expo_url = f'{host}{route}?title={urllib.parse.quote(news.title, safe = safe)}&url={urllib.parse.quote(news.url, safe = safe)}&img={urllib.parse.quote(news.img, safe = safe)}&favicon={urllib.parse.quote(news.website_favicon, safe = safe)}&website={urllib.parse.quote(news.website_name, safe = safe)}'

        print(expo_url)

        return render(request, 'redirect_to_app.html', {'redirect_url': expo_url})

class Screenshot(APIView):

    def get(self, request):
        favicon= request.GET.get('favicon')
        img= request.GET.get('img')
        website= request.GET.get('website')
        title= request.GET.get('title')
        date= request.GET.get('date')
        mode= request.GET.get('mode')
        
        return get_image(favicon, img, website, title, date, mode)
