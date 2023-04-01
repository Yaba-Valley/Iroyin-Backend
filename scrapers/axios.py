import myscrape


news= myscrape.scraper(website_link='https://www.axios.com/',
                        smallest_element_holding_image_text='div', 
                        class_of_smallest_element_holding_image_text='gtmView grid-layout border-b border-accent-blue-tint pb-6 sm:pb-10 last:border-b-0',
                        smallest_element_holding_text_link_alone='h2',
                        class_of_smallest_element_holding_text_link_alone='col-1-13 m-0',
                        favicon_url='myfav', 
                        website='web',
                        image_holder='src')
print(news)