import myscrape


news= myscrape.scraper(website_link='https://www.bloomberg.com/technology',
                        smallest_element_holding_image_text='article', 
                        class_of_smallest_element_holding_image_text='story-package-module__story mod-story',
                        smallest_element_holding_text_link_alone='a',
                        class_of_smallest_element_holding_text_link_alone='story-package-module__story__headline-link',
                        favicon_url='myfav', 
                        website='web',
                        image_holder='src')
print(news)