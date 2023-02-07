from re import T
from news.scraper.fashion import GlamourScraper, PeopleScraper
from news.scraper.health import VeryWellMindScraper
from news.scraper.sports import BundesligaScraper, EPLScraper, GoalDotComScraper, LaLigaScraper, PunchScraper, SkySportScraper
from news.scraper.tech import GlassDoorScraper, TechCrunchScraper, TechTrendsAfricaScraper, TheNextWebScraper


INTEREST_TO_SCRAPER_MAP = {
    'SPORTS': [
        PunchScraper(topic='sports'), 
        LaLigaScraper(), 
        GoalDotComScraper(),
        SkySportScraper(),
        EPLScraper(),
        BundesligaScraper(),
        TechCrunchScraper('sports')
    ],
    "POLITICS": [
        PunchScraper(topic = 'politics'),
        PeopleScraper(topic='politics'),
        TechCrunchScraper('politics'),
        TechCrunchScraper('nigeria'),
    ],
    "BUSINESS": [
        PunchScraper(topic='business'),
        TechCrunchScraper('business'),
        TechCrunchScraper('fintech'),
        TechCrunchScraper('plus'),
        TechTrendsAfricaScraper(category='business'),
        TechTrendsAfricaScraper(category='startups'),
        GlassDoorScraper(),
        TheNextWebScraper(category='growth-quarters'),
    ],
    "ENTERTAINMENT": [
        PunchScraper(topic='entertainment'),
        PeopleScraper(topic='entertainment'),
        TechCrunchScraper('entertainment'),
        GlamourScraper()
    ],
    "STARTUPS & FUNDING": [
        TechCrunchScraper('startups'),
        TechCrunchScraper('venture'),
        TechCrunchScraper('finance'),
        TechTrendsAfricaScraper(category='business'),
        TechTrendsAfricaScraper(category='startups'),                           
    ],
    "FASHION": [
        GlamourScraper(topic='skin'),
        GlamourScraper(topic='hair'),
        GlamourScraper(topic='makeup'),
        GlamourScraper(topic='fashion'),
        PeopleScraper(topic='fashion'),
        PeopleScraper(topic='beauty'),
        PeopleScraper(topic='style'),
        PeopleScraper(topic='shopping'),
    ],
    "CRYPTO": [
        TheNextWebScraper(category='hardfork'),
        TechCrunchScraper('crypto'),
        # NewsBlockScraper(),
        TechTrendsAfricaScraper(category='blockchain')
    ],
    "HEALTH": [
        VeryWellMindScraper(),
        PeopleScraper(topic = 'health'),
        GlamourScraper(topic = 'wellness')   
    ],
    'TECH': [
        TechCrunchScraper('apps'),
        TechCrunchScraper('hardware'),
        TechCrunchScraper('security'),
    ],
    'PROGRAMMING': [],
    'MEN\'S FASHION': [],
    'WOMEN\'S FASHION': [],
    'AFRICA': [],
    'NIGERIA': [],
    'LOCAL': [],
    'GLOBAL': [],
    
}
