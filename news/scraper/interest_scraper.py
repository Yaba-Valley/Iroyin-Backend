from news.scraper.fashion import GlamourScraper, PeopleScraper
from news.scraper.health import VeryWellMindScraper, VeryWellHealthScraper, VeryWellFamilyScraper, VeryWellFitScraper
from news.scraper.sports import BundesligaScraper, EPLScraper, GoalDotComScraper, LaLigaScraper, PunchScraper, SkySportScraper
from news.scraper.tech import GlassDoorScraper, TechCrunchScraper, TechTrendsAfricaScraper, TheNextWebScraper, FreeCodeCampScraper, BitcoinNewsScraper
from news.scraper.finance import FinanceSamuraiScraper, InvestopediaScraper, ForbesScraper


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
        PunchScraper(topic='politics'),
        PeopleScraper(topic='politics'),
        TechCrunchScraper('politics'),
        TechCrunchScraper('nigeria'),
        InvestopediaScraper('political-news'),
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
        InvestopediaScraper('economic-news')
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
        InvestopediaScraper('company-news'),
        ForbesScraper('business'),
        ForbesScraper('small-business'),
        ForbesScraper('world-billionaires'),
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
        ForbesScraper('lifestyle')
    ],
    "CRYPTO": [
        TheNextWebScraper(category='hardfork'),
        TechCrunchScraper('crypto'),
        BitcoinNewsScraper(),
        # NewsBlockScraper(),
        TechTrendsAfricaScraper(category='blockchain'),
        InvestopediaScraper('crypto-news')
    ],
    "HEALTH": [
        VeryWellMindScraper(),
        VeryWellHealthScraper(),
        VeryWellFamilyScraper(),
        VeryWellFitScraper(),
        PeopleScraper(topic='health'),
        GlamourScraper(topic='wellness')
    ],
    'TECH': [
        TechCrunchScraper('apps'),
        TechCrunchScraper('hardware'),
        TechCrunchScraper('security'),
        ForbesScraper('innovation'),
    ],
    'FINANCE': [
        FinanceSamuraiScraper(),
        InvestopediaScraper('market-news'),
        InvestopediaScraper('personal-finance-news'),
        ForbesScraper('leadership'),
        ForbesScraper('money'),
    ],
    'REAL ESTATE': [
        ForbesScraper('real-estate'),
    ],
    'PROGRAMMING': [
        FreeCodeCampScraper()
    ],
    'MEN\'S FASHION': [],
    'WOMEN\'S FASHION': [],
    'AFRICA': [],
    'NIGERIA': [],
    'LOCAL': [],
    'GLOBAL': [],

}
