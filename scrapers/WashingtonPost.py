import myscrape


news= myscrape.scraper(website_link='https://www.washingtonpost.com/world/?itid=nb_world',
                        smallest_element_holding_image_text='div', 
                        class_of_smallest_element_holding_image_text='w-100 grid',
                        smallest_element_holding_text_link_alone='a',
                        class_of_smallest_element_holding_text_link_alone='flex hover-blue',
                        favicon_url='myfav', 
                        website='web',
                        image_holder='src',
                        lazyload_images=True)
print(news)