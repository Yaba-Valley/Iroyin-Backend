from tkinter import Scrollbar
from django.test import TestCase
from . import scraper

# Create your tests here.

class TestScraper(TestCase):
    
    def test_punch_scraper(self):
        
        """ 
        Test if the punch scraper return scraped news 
        NOTE THAT THIS SCRAPER REQUIRES A TOPIC
        """
        
        scraped_news = scraper.PunchScraper('business').scrape()
        
        self.assertNotEqual(len(scraped_news), 0, 'Punch Scraper does not return anything')
        
    def test_vanguard_scraper(self):
        
        """ 
        Test if the vanguard scraper return more than 1 news 
        NOTE THAT THIS SCRAPER REQUIRES A TOPIC
        """
        
        scraped_news = scraper.VanguardScraper('business').scrape()
        
        self.assertNotEqual(len(scraped_news), 0, 'Vanguard Scraper does not return anything')
        
    
    def test_goal_dot_com_scaper(self):
        
        """
            Test that the GOALDOTCOM Scraper returns more than 1 news
            NOTE: THIS SCRAPER DOESN'T REQUIRE A TOPIC
        """
        scraped_news = scraper.GoalDotComScraper().scrape()
        
        self.assertNotEqual(len(scraped_news), 0, 'goal.com scaper does not return anything')
        
    def test_sky_sport_scraper(self):
        
        """ 
            This test ensures that the skysport scraper returns more than one news
            NOTE: THIS SCRAPER DOESN'T REQUIRE A TOPIC 
        """
        scraped_news = scraper.SkySportScraper().scrape()
        
        self.assertNotEqual(len(scraped_news), 0, 'skysports scraper does not return anything')
        
    
    def test_epl_scaper(self):
        """ 
            This test ensures the epl scraper returns more than one news
            NOTE: THIS SCRAPER DOESN'T REQUIRE A TOPIC
        """
        
        scraped_news = scraper.EPLScraper().scrape()
        
        self.assertNotEqual(len(scraped_news), 0, 'epl scraper does not return anything')
        
    
    def test_laliga_scraper(self):
        """ 
            This test ensure that the laliga scraper returns more than one news
            NOTE: THIS SCRAPER DOESN'T REQUIRE A TOPIC
        """
        
        scraped_news = scraper.LaLigaScraper().scrape()
        
        self.assertNotEqual(len(scraped_news), 0, 'la liga scraper does not return anything')
        
    def test_bundesliga_scraper(self):
        """ 
            This test ensure that the bundesliga scraper returns more than one news
            NOTE: THIS SCRAPER DOESN'T REQUIRE A TOPIC
        """
        
        scraped_news = scraper.BundesligaScraper().scrape()
        
        self.assertNotEqual(len(scraped_news), 0, 'bundesliga scraper does not return anything')
        
    def test_freecodecamp_scraper(self):
        """ 
            This test ensure that the freecodecamp scraper returns more than one news
            NOTE: THIS SCRAPER DOESN'T REQUIRE A TOPIC
        """
        
        scraped_news = scraper.FreeCodeCampScraper().scrape()
        
        self.assertNotEqual(len(scraped_news), 0, 'freecodecamp scraper does not return anything')
        
    def test_techcrunch_scraper(self):
        """ 
            This test ensures that the techcrunch scraper returns more than one news
            NOTE: THIS SCRAPER DOESN'T REQUIRE A TOPIC
        """
        
        scraped_news = scraper.TechCrunchScraper().scrape()
        self.assertNotEqual(len(scraped_news), 0, 'techcrunch scraper does not return anything')