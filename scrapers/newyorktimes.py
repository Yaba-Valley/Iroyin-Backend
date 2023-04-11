import myscrape


news= myscrape.scraper(website_link='https://www.nytimes.com/section/world',
                        smallest_element_holding_image_text='article', 
                        class_of_smallest_element_holding_image_text='css-15cbhtu',
                        smallest_element_holding_text_link_alone='h2',
                        class_of_smallest_element_holding_text_link_alone='css-14g652u e1y0a3kv0',
                        favicon_url='myfav', 
                        website='web',
                        image_holder='src')
print(news)