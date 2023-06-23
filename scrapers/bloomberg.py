from scrapers import myscrape
from news.models import Website
import requests

website_text = requests.get('https://www.financialsamurai.com/', headers={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Cookie': 'tnw_morph=973357127; tfv=2022-09-29T18:52:23.395+01:00; gdpr-auditId=fad5b09eed7c4dfb855caaaaa25eb995; __gads=ID=358254a7976f22ff:T=1664473946:S=ALNI_MZNOlKY6jdXhmMEFheTmuSSWNQRtg; __gpi=UID=00000af0d6b42650:T=1664473946:RT=1664473946:S=ALNI_MYHrIOXf1xBZo_gtbQmLFrsy_z5rQ; __hstc=111399067.cc4094bf9ee50368559c2ffc942bc67e.1664473954009.1664473954009.1664473954009.1; hubspotutk=cc4094bf9ee50368559c2ffc942bc67e; tlv=2022-09-29T18:56:02.713+01:00; _ga=GA1.1.1246751966.1664473946; _ga_1FX48DMMCB=GS1.1.1664473947.1.1.1664475231.0.0.0'
}).text


news = myscrape.scraper(
    website_text=website_text,
    website_name='FinanceSamurai',
    website_object=Website.objects.last(),
    smallest_article_element='li',
    class_of_smallest_article_element='',
    smallest_image_element='img',
    class_of_smallest_image_element='entry-image attachment-post',
    smallest_link_element_with_class='h2',
    class_of_smallest_link_element='entry-title',
    smallest_title_element='h2',
    class_of_smallest_title_element='entry-title',
    prepend_image_url='',
    prepend_url='',
    image_holder_attr='data-lazy-srcset',
    favicon='https://i2.wp.com/financialsamurai.com/wp-content/uploads/2017/02/cropped-FinancialSamurai-Site-Icon-700x700-180x180.png'
)

print(news)
