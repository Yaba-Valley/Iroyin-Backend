import myscrape
import requests


# news= myscrape.scraper(website_link='https://www.nytimes.com/section/world',
#                         smallest_element_holding_image_text='article', 
#                         class_of_smallest_element_holding_image_text='css-15cbhtu',
#                         smallest_element_holding_text_link_alone='h2',
#                         class_of_smallest_element_holding_text_link_alone='css-14g652u e1y0a3kv0',
#                         favicon_url='myfav', 
#                         website='web',
#                         image_holder='src')
# print(news)


request_text = requests.get('https://www.healthline.com/mental-health').text

news = myscrape.scraper(
    website_text=request_text,
    smallest_article_element='li',
    class_of_smallest_article_element='css-1ib8oek',
    smallest_link_element_with_class='a',
    class_of_smallest_link_element='css-16e3huk',
    smallest_image_element='lazy-image',
    class_of_smallest_image_element='css-10vopkp',
    image_holder_attr='src',
    smallest_title_element='a',
    class_of_smallest_title_element='css-16e3huk',
    prepend_url='https://www.healthline.com',
    favicon='',
    website_name='Healthline',
    website_object={}
)

print(news)

