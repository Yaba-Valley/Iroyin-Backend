from bs4 import BeautifulSoup 
import requests

headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Cookie': 'tnw_morph=973357127; tfv=2022-09-29T18:52:23.395+01:00; gdpr-auditId=fad5b09eed7c4dfb855caaaaa25eb995; __gads=ID=358254a7976f22ff:T=1664473946:S=ALNI_MZNOlKY6jdXhmMEFheTmuSSWNQRtg; __gpi=UID=00000af0d6b42650:T=1664473946:RT=1664473946:S=ALNI_MYHrIOXf1xBZo_gtbQmLFrsy_z5rQ; __hstc=111399067.cc4094bf9ee50368559c2ffc942bc67e.1664473954009.1664473954009.1664473954009.1; hubspotutk=cc4094bf9ee50368559c2ffc942bc67e; tlv=2022-09-29T18:56:02.713+01:00; _ga=GA1.1.1246751966.1664473946; _ga_1FX48DMMCB=GS1.1.1664473947.1.1.1664475231.0.0.0'
        }

def scraper(website_link, smallest_element_holding_image_text, 
            class_of_smallest_element_holding_image_text, 
            smallest_element_holding_text_link_alone, 
            class_of_smallest_element_holding_text_link_alone,
            favicon_url,
            website,
            image_holder,
            index_holding_title=0,
            lazyload_images=False
            ):
    
    '''
    image_holder=data-src or src or data-gl-src
    '''
    response_text= requests.get(website_link, headers=headers).text
    content= BeautifulSoup(response_text, 'html.parser')

    print(content.find_all(smallest_element_holding_image_text,{'class':class_of_smallest_element_holding_image_text})[8].text)
    news_section= content.find_all(smallest_element_holding_image_text, {'class':class_of_smallest_element_holding_image_text})

    if smallest_element_holding_text_link_alone != 'a':
        result=[{
            'title': i.find(smallest_element_holding_text_link_alone, {'class':class_of_smallest_element_holding_text_link_alone}, ).text.strip(), 
            'url':i.find(smallest_element_holding_text_link_alone, {'class':class_of_smallest_element_holding_text_link_alone}).find('a')['href'], #fix
            'img':i.find('img')[image_holder], 
            'metadata': {'website': website, 'favicon': favicon_url}
            } for i in news_section if i.find('img') != None ]
    elif (smallest_element_holding_image_text==smallest_element_holding_text_link_alone) and (class_of_smallest_element_holding_image_text==class_of_smallest_element_holding_text_link_alone):
        result=[{
            'title': i.text.strip(), 
            'url':i['href'], #fix
            'img':i.find('img')[image_holder], 
            'metadata': {'website': website, 'favicon': favicon_url}
            } for i in news_section if i.find('img') != None ]    
    else:
        print("ELSE")
        if lazyload_images==False:
            result=[{
                'title': i.find_all(smallest_element_holding_text_link_alone, {'class':class_of_smallest_element_holding_text_link_alone} )[index_holding_title].text.strip().replace('\xad', ''), 
                'url':i.find(smallest_element_holding_text_link_alone, {'class':class_of_smallest_element_holding_text_link_alone})['href'], #fix
                'img':i.find('img')[image_holder], 
                'metadata': {'website': website, 'favicon': favicon_url}
                } for i in news_section if i.find('img') != None ]
        else:
            result=[{
                'title': i.find_all(smallest_element_holding_text_link_alone, {'class':class_of_smallest_element_holding_text_link_alone} )[index_holding_title].text.strip().replace('\xad', ''), 
                'url':i.find(smallest_element_holding_text_link_alone, {'class':class_of_smallest_element_holding_text_link_alone})['href'], 
                'metadata': {'website': website, 'favicon': favicon_url}
                } for i in news_section ]
    return result