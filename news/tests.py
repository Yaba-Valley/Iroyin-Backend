from tkinter import Scrollbar
from django.test import TestCase
from . import scraper
from .utils import fetch_news_async
import asyncio

# Create your tests here.

class TestScraper(TestCase):
    
    def test_punch_scraper(self):
        
        """ 
        Test if the punch scraper return scraped news 
        NOTE THAT THIS SCRAPER REQUIRES A TOPIC
        """
        
        scraped_news = asyncio.run(fetch_news_async([scraper.PunchScraper('business')]))
        
        self.assertNotEqual(len(scraped_news), 0, 'Punch Scraper does not return anything')
        
    def test_vanguard_scraper(self):
        
        """ 
        Test if the vanguard scraper return more than 1 news 
        NOTE THAT THIS SCRAPER REQUIRES A TOPIC
        """
        
        scraped_news = asyncio.run(fetch_news_async([scraper.VanguardScraper('business')]))
        
        self.assertNotEqual(len(scraped_news), 0, 'Vanguard Scraper does not return anything')
        
    
    def test_goal_dot_com_scaper(self):
        
        """
            Test that the GOALDOTCOM Scraper returns more than 1 news
            NOTE: THIS SCRAPER DOESN'T REQUIRE A TOPIC
        """
        scraped_news = asyncio.run(fetch_news_async([scraper.GoalDotComScraper()]))
        
        self.assertNotEqual(len(scraped_news), 0, 'goal.com scaper does not return anything')
        
    def test_sky_sport_scraper(self):
        
        """ 
            This test ensures that the skysport scraper returns more than one news
            NOTE: THIS SCRAPER DOESN'T REQUIRE A TOPIC 
        """
        scraped_news = asyncio.run(fetch_news_async([scraper.SkySportScraper()]))
        
        self.assertNotEqual(len(scraped_news), 0, 'skysports scraper does not return anything')
        
    
    def test_epl_scaper(self):
        """ 
            This test ensures the epl scraper returns more than one news
            NOTE: THIS SCRAPER DOESN'T REQUIRE A TOPIC
        """
        
        scraped_news = asyncio.run(fetch_news_async([scraper.EPLScraper()]))
        
        self.assertNotEqual(len(scraped_news), 0, 'epl scraper does not return anything')
        
    
    def test_laliga_scraper(self):
        """ 
            This test ensure that the laliga scraper returns more than one news
            NOTE: THIS SCRAPER DOESN'T REQUIRE A TOPIC
        """
        
        scraped_news = asyncio.run(fetch_news_async([scraper.LaLigaScraper()]))
        
        self.assertNotEqual(len(scraped_news), 0, 'la liga scraper does not return anything')
        
    def test_bundesliga_scraper(self):
        """ 
            This test ensure that the bundesliga scraper returns more than one news
            NOTE: THIS SCRAPER DOESN'T REQUIRE A TOPIC
        """
        
        scraped_news = asyncio.run(fetch_news_async([scraper.BundesligaScraper()]))
        
        self.assertNotEqual(len(scraped_news), 0, 'bundesliga scraper does not return anything')
        
    def test_freecodecamp_scraper(self):
        """ 
            This test ensure that the freecodecamp scraper returns more than one news
            NOTE: THIS SCRAPER DOESN'T REQUIRE A TOPIC
        """
        
        scraped_news = asyncio.run(fetch_news_async([scraper.FreeCodeCampScraper()]))
        
        self.assertNotEqual(len(scraped_news), 0, 'freecodecamp scraper does not return anything')
        
    def test_techcrunch_scraper(self):
        """ 
            This test ensures that the techcrunch scraper returns more than one news
            NOTE: THIS SCRAPER DOESN'T REQUIRE A TOPIC
        """
        
        scraped_news = asyncio.run(fetch_news_async([scraper.TechCrunchScraper(isNigeria=True, isStartups=True)]))
        self.assertNotEqual(len(scraped_news), 0, 'techcrunch scraper does not return anything')
        
    
    def test_techtrends_scraper(self):
        """
            This test whether the techtrendsafrica scraper returns more than one news or not
        """
        
        scraped_news = asyncio.run(fetch_news_async([scraper.TechTrendsAfricaScraper(category='startups')]))
        self.assertNotEqual(len(scraped_news), 0, 'techtrends scraper does not return anything')
        
    
    def test_gizmodo_scraper(self):
        """
            This test the number of news returned by the gizmodo scraper, fails if the 
            scraper returns no news
        """
        
        scraped_news = asyncio.run(fetch_news_async([scraper.GizModoScraper()]))
        self.assertNotEqual(len(scraped_news), 0, 'gizmodo scraper does not return anything')
        
    def test_newsblock_scraper(self):
        """
            This test the number of news returned by the newsblock scraper, fails if the 
            scraper returns no news
        """
        
        scraped_news = asyncio.run(fetch_news_async([scraper.NewsBlockScraper()]))
        self.assertNotEqual(len(scraped_news), 0, 'newsblock scraper does not return anything')