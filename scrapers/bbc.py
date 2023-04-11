import myscrape


news= myscrape.scraper(website_link='https://www.bbc.com/news/world',
                        smallest_element_holding_image_text='div', 
                        class_of_smallest_element_holding_image_text='gs-c-promo gs-t-News nw-c-promo gs-o-faux-block-link gs-u-pb gs-u-pb+@m nw-p-default gs-c-promo--inline gs-c-promo--stacked@m gs-c-promo--flex',
                        smallest_element_holding_text_link_alone='a',
                        class_of_smallest_element_holding_text_link_alone='gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor',
                        favicon_url='myfav', 
                        website='web',
                        image_holder='data-src')
print(news)