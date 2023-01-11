from django.test import TestCase
from . import scraper
from .utils import fetch_news_async
import asyncio

def run_test(testcase, scraper):
    news = []
    scraped_news = asyncio.run(fetch_news_async([scraper], news))
    print(scraper.name, 'returns', len(scraped_news), 'news\n\n')
    testcase.assertNotEqual(len(scraped_news), 0, '{0} does not return anything'.format(scraper.name))

class TestScraper(TestCase):
    
    def test_glamour_scraper(self):
        run_test(self, scraper.GlamourScraper('entertainment'))
        
    def test_people_scraper(self):
        run_test(self, scraper.PeopleScraper('entertainment'))
    
    def test_punch_scraper(self):
        run_test(self, scraper.PunchScraper('sports'))
        
    def test_very_well_mind_scraper(self):
        run_test(self, scraper=scraper.VeryWellMindScraper())
    
    def test_vanguard_scraper(self):
        run_test(self, scraper=scraper.VanguardScraper())
        
    def test_goal_dot_com_scraper(self):
        run_test(self, scraper=scraper.GoalDotComScraper())
        
    def test_sky_sport_scraper(self):
        run_test(self, scraper=scraper.SkySportScraper())
    
    def test_epl_scraper(self):
        run_test(self, scraper=scraper.EPLScraper())
        
    def test_laliga_scraper(self):
        run_test(self, scraper=scraper.LaLigaScraper())
    
    def test_bundesliga_scraper(self):
        run_test(self, scraper=scraper.BundesligaScraper())
    
    def test_free_code_camp_scraper(self):
        run_test(self, scraper=scraper.FreeCodeCampScraper())
    
    def test_techcrunch_scraper(self):
        run_test(self, scraper=scraper.TechCrunchScraper(isNigeria=True, isStartups=True))
    
    def test_techtrendsafrica_scraper(self):
        run_test(self, scraper=scraper.TechTrendsAfricaScraper(category='startups'))
        
    def test_gizmodo_scraper(self):
        run_test(self, scraper=scraper.GizModoScraper())
    
    def test_thenextweb_scraper(self):
        run_test(self, scraper=scraper.TheNextWebScraper())
    
    def test_glassdoor_scraper(self):
        run_test(self, scraper=scraper.GlassDoorScraper())
    
    def test_news_block_scraper(self):
        run_test(self, scraper=scraper.NewsBlockScraper())
        