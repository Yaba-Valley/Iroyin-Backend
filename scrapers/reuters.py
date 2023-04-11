import myscrape


result= myscrape.scraper(website_link='https://www.reuters.com/world/',
                         smallest_element_holding_image_text='div',
                         class_of_smallest_element_holding_image_text='media-story-card__hub__3mHOR story-card',
                         smallest_element_holding_text_link_alone='a',
                         class_of_smallest_element_holding_text_link_alone='text__text__1FZLe text__dark-grey__3Ml43 text__medium__1kbOh text__heading_5_and_half__3YluN heading__base__2T28j heading_5_half media-story-card__heading__eqhp9',
                         favicon_url='any',
                         website='CNN',
                         image_holder='src',
                         index_holding_title=0,
                         lazyload_images=True)

print(result)