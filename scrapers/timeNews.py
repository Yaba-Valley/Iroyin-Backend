import myscrape


news= myscrape.scraper(website_link='http://time.com',
                        smallest_element_holding_image_text='a', 
                        class_of_smallest_element_holding_image_text='tout__list-item-link',
                        smallest_element_holding_text_link_alone='a',
                        class_of_smallest_element_holding_text_link_alone='tout__list-item-link',
                        favicon_url='myfav', 
                        website='web',
                        image_holder='src')
print(news)