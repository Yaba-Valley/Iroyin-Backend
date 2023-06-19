from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Cookie': 'tnw_morph=973357127; tfv=2022-09-29T18:52:23.395+01:00; gdpr-auditId=fad5b09eed7c4dfb855caaaaa25eb995; __gads=ID=358254a7976f22ff:T=1664473946:S=ALNI_MZNOlKY6jdXhmMEFheTmuSSWNQRtg; __gpi=UID=00000af0d6b42650:T=1664473946:RT=1664473946:S=ALNI_MYHrIOXf1xBZo_gtbQmLFrsy_z5rQ; __hstc=111399067.cc4094bf9ee50368559c2ffc942bc67e.1664473954009.1664473954009.1664473954009.1; hubspotutk=cc4094bf9ee50368559c2ffc942bc67e; tlv=2022-09-29T18:56:02.713+01:00; _ga=GA1.1.1246751966.1664473946; _ga_1FX48DMMCB=GS1.1.1664473947.1.1.1664475231.0.0.0'
}


def scraper(website_text,
            smallest_article_element,
            class_of_smallest_article_element,
            smallest_link_element_with_class,
            class_of_smallest_link_element,
            smallest_image_element,
            class_of_smallest_image_element,
            image_holder_attr,
            smallest_title_element,
            class_of_smallest_title_element,
            favicon,
            website_name,
            website_object,
            prepend_image_url='',
            prepend_url='',
            ):
    
    soup = BeautifulSoup(website_text, 'html.parser')

    all_articles = soup.find_all(
        smallest_article_element, class_=class_of_smallest_article_element)

    print('hello', len(all_articles))

    results = []

    for article in all_articles:
        try:
            title = article.find(smallest_title_element,
                                 class_=class_of_smallest_title_element).text.strip()
            
            print(title)

            if smallest_link_element_with_class != 'a':
                url = prepend_url+article.find(smallest_link_element_with_class,
                                               class_=class_of_smallest_link_element).find('a').attrs.get('href')
            elif (class_of_smallest_link_element == class_of_smallest_article_element) and (smallest_link_element_with_class == smallest_article_element):
                url = prepend_url + article.attrs.get('href')
            else:
                url = prepend_url+article.find(smallest_link_element_with_class,
                                               class_=class_of_smallest_link_element).attrs.get('href')
            print(url)
            
            if image_holder_attr == 'style':
                image = article.find(smallest_image_element, class_=class_of_smallest_image_element).attrs.get(
                    'style').split('url(')[-1].split(')')[0]
            else:
                if smallest_image_element != 'img':
                    image = article.find(smallest_image_element,
                                         class_=class_of_smallest_image_element).find('img').attrs.get(image_holder_attr or 'src')
                else:
                    image = prepend_image_url + article.find(
                        smallest_image_element, class_=class_of_smallest_image_element).attrs.get(image_holder_attr or 'src')

                if image_holder_attr.__contains__('srcset'):
                    image = prepend_image_url + \
                        image.split(', ')[-1].strip().split(' ')[0]

            image = image.split('?')[0]
            if image.__contains__('c_fill,f_auto,g_center,h_80,q_60,w_80'):
                image = image.split('/c_fill,f_auto,g_center,h_80,q_60,w_80')[
                    0] + image.split('/c_fill,f_auto,g_center,h_80,q_60,w_80')[1]
                
            print(image)

            article = {
                'title': title,
                'url': url,
                'img': image,
                'website': website_object
            }

            results.append(article)

        except Exception as e:
            print('the error is', e)

    # print(results)
    return results


# from news.utils import test_scraper; from scrapers.finance import InvestopediaScraper; test_scraper(InvestopediaScraper())
