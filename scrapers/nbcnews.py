import myscrape
import requests

website_text = requests.get('https://www.nbcnews.com/world').text

result= myscrape.scraper(website_text=website_text,
                         smallest_element_holding_image_text='div',
                         class_of_smallest_element_holding_image_text='wide-tease-item__info-wrapper flex-grow-1-m',
                         smallest_element_holding_text_link_alone='a',
                         class_of_smallest_element_holding_text_link_alone=None,
                         favicon_url='any',
                         website='CNN',
                         image_holder='src',
                         index_holding_title=1)

print(result)

