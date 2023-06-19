from scrapers import myscrape
from news.models import Website
import requests

website_text = requests.get('https://people.com/tag/news/', headers={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Cookie': 'tnw_morph=973357127; tfv=2022-09-29T18:52:23.395+01:00; gdpr-auditId=fad5b09eed7c4dfb855caaaaa25eb995; __gads=ID=358254a7976f22ff:T=1664473946:S=ALNI_MZNOlKY6jdXhmMEFheTmuSSWNQRtg; __gpi=UID=00000af0d6b42650:T=1664473946:RT=1664473946:S=ALNI_MYHrIOXf1xBZo_gtbQmLFrsy_z5rQ; __hstc=111399067.cc4094bf9ee50368559c2ffc942bc67e.1664473954009.1664473954009.1664473954009.1; hubspotutk=cc4094bf9ee50368559c2ffc942bc67e; tlv=2022-09-29T18:56:02.713+01:00; _ga=GA1.1.1246751966.1664473946; _ga_1FX48DMMCB=GS1.1.1664473947.1.1.1664475231.0.0.0'
}).text


news = myscrape.scraper(
    website_text=website_text,
    website_name='People',
    website_object=Website.objects.last(),
    smallest_article_element='a',
    class_of_smallest_article_element='mntl-document-card',
    smallest_image_element='img',
    class_of_smallest_image_element='lazyload card__img universal-image__image',
    smallest_link_element_with_class='a',
    class_of_smallest_link_element='mntl-document-card',
    smallest_title_element='span',
    class_of_smallest_title_element='card__title-text',
    prepend_image_url='',
    prepend_url='',
    image_holder_attr='data-src',
    favicon='https://people.com/img/favicons/favicon-152.png'
)

print(news)
