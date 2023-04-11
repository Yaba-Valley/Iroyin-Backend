import myscrape


result= myscrape.scraper(website_link='https://www.aljazeera.com/news/',
                         smallest_element_holding_image_text='article',
                         class_of_smallest_element_holding_image_text='gc u-clickable-card gc--type-post gc--list gc--with-image',
                         smallest_element_holding_text_link_alone='a',
                         class_of_smallest_element_holding_text_link_alone='u-clickable-card__link',
                         favicon_url='any',
                         website='CNN',
                         image_holder='src',
                         index_holding_title=0)


fearured_news= myscrape.scraper(website_link='https://www.aljazeera.com/news/',
                         smallest_element_holding_image_text='article',
                         class_of_smallest_element_holding_image_text='gc u-clickable-card gc--type-post css-0 gc--with-image',
                         smallest_element_holding_text_link_alone='a',
                         class_of_smallest_element_holding_text_link_alone='u-clickable-card__link',
                         favicon_url='any',
                         website='CNN',
                         image_holder='src',
                         index_holding_title=0)
print(result)
print(fearured_news)