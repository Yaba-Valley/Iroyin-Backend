from re import T
from news.scraper.fashion import GlamourScraper, PeopleScraper
from news.scraper.sports import BundesligaScraper, EPLScraper, GoalDotComScraper, LaLigaScraper, PunchScraper, SkySportScraper
from news.scraper.tech import GlassDoorScraper, NewsBlockScraper, TechCrunchScraper, TechTrendsAfricaScraper, TheNextWebScraper


interest_to_scraper_map = {
    'SPORTS': [
        PunchScraper(topic='sports'), 
        LaLigaScraper(), 
        GoalDotComScraper(),
        SkySportScraper(),
        EPLScraper(),
        BundesligaScraper()
    ],
    "POLITICS": [
        PunchScraper(topic = 'politics'),
        PeopleScraper(topic='politics'),
    ],
    "BUSINESS": [
        PunchScraper(topic='business'),
        TechCrunchScraper(isNigeria=True, isStartups=False),
        TechCrunchScraper(isNigeria=False, isStartups=True),
        TechTrendsAfricaScraper(category='business'),
        TechTrendsAfricaScraper(category='startups'),
        GlassDoorScraper(),
        TheNextWebScraper(category='growth-quarters')
    ],
    "ENTERTAINMENT": [
        PunchScraper(topic='entertainment'),
        PeopleScraper(topic='entertainment'),
        GlamourScraper()
    ],
    "STARTUPS & FUNDING": [
        TechCrunchScraper(isNigeria=True, isStartups=False),
        TechCrunchScraper(isNigeria=False, isStartups=True),
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
        NewsBlockScraper(),
        TechTrendsAfricaScraper(category='blockchain')
    ],
    "HEALTH": [
        
    ]
}
