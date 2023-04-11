import myscrape

print(myscrape.scraper(website_link='https://www.usatoday.com/',
                       smallest_element_holding_image_text='a', 
                        class_of_smallest_element_holding_image_text='gnt_m_sl_a gnt_m_sl_a__nlc',
                        smallest_element_holding_text_link_alone='a',
                        class_of_smallest_element_holding_text_link_alone='gnt_m_sl_a gnt_m_sl_a__nlc',
                        favicon_url='myfav', 
                        website='web',
                        image_holder='data-gl-src')
                        )