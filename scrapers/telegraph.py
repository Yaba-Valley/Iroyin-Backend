import myscrape

result= myscrape.scraper(website_link='https://www.telegraph.co.uk/news/',
                         smallest_element_holding_image_text='article',
                         class_of_smallest_element_holding_image_text='card u-clickable-area card--feature card--premium',
                         smallest_element_holding_text_link_alone='a',
                         class_of_smallest_element_holding_text_link_alone='list-headline__link u-clickable-area__link',
                         favicon_url='any',
                         website='CNN',
                         image_holder='src',
                         index_holding_title=0)

print(result)

