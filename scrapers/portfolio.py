import myscrape
import requests

text = requests.get('https://www.wsj.com/').text

news = myscrape.scraper(text, 'article', 'WSJTheme--story--XB4V2mLz WSJTheme--story-padding--1gRL3tuf WSJTheme--border-bottom--s4hYCt0s ', 'a', None, 'favicon', 'wallstreetjournal', 'src', 0, True)

print(news)
