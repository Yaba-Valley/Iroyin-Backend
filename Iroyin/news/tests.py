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
        
        self.assertNotEqual(len(scraped_news), 0, 'Punch Scraper works perfectly')
        
    def test_vanguard_scraper(self):
        
        """ 
        Test if the vanguard scraper return more than 1 news 
        NOTE THAT THIS SCRAPER REQUIRES A TOPIC
        """
        
        scraped_news = scraper.VanguardScraper('business').scrape()
        
        self.assertNotEqual(len(scraped_news), 0, 'Vanguard Scraper works perfectly')
        
    
    def test_goal_dot_com_scaper(self):
        
        """
            Test is the GOALDOTCOM Scraper returns more than 1 news
            NOTE: THIS SCRAPER DOESN'T REQUIRE A TOPIC
        """
        scraped_news = scraper.GoalDotComScraper().scrape()
        
        self.assertNotEqual(len(scraped_news), 0, 'goal.com scaper works perfectly')
        
    
