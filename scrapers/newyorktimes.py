from scrapers import myscrape
from news.models import Website
import requests


request_text = requests.get('https://www.healthline.com/mental-health/mind-and-body').text

news = myscrape.scraper(
    website_text=request_text,
    smallest_article_element='li',
    class_of_smallest_article_element='css-1ib8oek',
    smallest_link_element_with_class='a',
    class_of_smallest_link_element='css-16e3huk',
    smallest_image_element='lazy-image',
    class_of_smallest_image_element='',
    image_holder_attr='src',
    smallest_title_element='a',
    class_of_smallest_title_element='css-16e3huk',
    prepend_url='https://www.healthline.com',
    prepend_image_url='https://',
    favicon='',
    website_name='Healthline',
    website_object=Website.objects.last()
)

print(news)

