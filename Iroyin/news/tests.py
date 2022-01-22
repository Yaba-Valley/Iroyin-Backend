from django.test import TestCase
from . import scraper

# Create your tests here.

class TestScraper(TestCase):
    
    def test_punch_scraper(self):
        
        """ Test if the punch scraper return scraped news """
        
        scraped_news = scraper.PunchScraper('business').scrape()
        
        self.assertNotEqual(len(scraped_news), 0, 'Length of scraped news should not be 0')
        
    
