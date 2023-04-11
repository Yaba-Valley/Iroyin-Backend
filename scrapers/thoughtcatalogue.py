import myscrape


news= myscrape.scraper(website_link='https://thoughtcatalog.com/',
                        smallest_element_holding_image_text='article', 
                        class_of_smallest_element_holding_image_text='preview is-layout-network',
                        smallest_element_holding_text_link_alone='a',
                        class_of_smallest_element_holding_text_link_alone='preview__permalink',
                        favicon_url='myfav', 
                        website='web',
                        image_holder='src')
print(news)