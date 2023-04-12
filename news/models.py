from django.db import models
from scrapers import myscrape

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Cookie': 'tnw_morph=973357127; tfv=2022-09-29T18:52:23.395+01:00; gdpr-auditId=fad5b09eed7c4dfb855caaaaa25eb995; __gads=ID=358254a7976f22ff:T=1664473946:S=ALNI_MZNOlKY6jdXhmMEFheTmuSSWNQRtg; __gpi=UID=00000af0d6b42650:T=1664473946:RT=1664473946:S=ALNI_MYHrIOXf1xBZo_gtbQmLFrsy_z5rQ; __hstc=111399067.cc4094bf9ee50368559c2ffc942bc67e.1664473954009.1664473954009.1664473954009.1; hubspotutk=cc4094bf9ee50368559c2ffc942bc67e; tlv=2022-09-29T18:56:02.713+01:00; _ga=GA1.1.1246751966.1664473946; _ga_1FX48DMMCB=GS1.1.1664473947.1.1.1664475231.0.0.0'
}


class Interest(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Website(models.Model):
    general_name = models.CharField(max_length=500, verbose_name='Name')
    sub_category = models.CharField(max_length=100)
    categories = models.ManyToManyField(
        to=Interest, related_name='websites', verbose_name='Categories')
    website_favicon = models.URLField(
        verbose_name='Favicon', default='https://media.istockphoto.com/vectors/news-vector-id918880270?k=20&m=918880270&s=612x612&w=0&h=bDcgr9jhiRYCPMUhVdLKD5ouIc5daM4qMcaPPapppQI=')
    website_url = models.URLField(verbose_name='URL')

    # fields for the scraping function
    smallest_article_element = models.CharField(
        max_length=10, verbose_name='News Container HTML Element', default='')
    class_of_smallest_article_element = models.CharField(
        max_length=500, verbose_name='Class of News Container HTML Element', default='', blank=True)
    smallest_link_element = models.CharField(
        max_length=10, verbose_name='News Link HTML Element', default='')
    class_of_smallest_link_element = models.CharField(
        max_length=500, verbose_name='Class of News Link HTML Element', default='', blank=True)
    smallest_image_element = models.CharField(
        max_length=10, verbose_name='News Image HTML Element', default='')
    class_of_smallest_image_element = models.CharField(
        max_length=500, verbose_name='Class of News Image HTML Element', default='', blank=True)
    smallest_title_element = models.CharField(
        max_length=10, verbose_name='News title HTML Element', default='')
    class_of_smallest_title_element = models.CharField(
        max_length=500, verbose_name='Class of News title HTML Element', default='', blank=True)
    image_holder_attr = models.CharField(
        max_length=500, verbose_name='Image Holder Attribute (src,data-src,srcset,etc.)', default='src')
    preprend_image_url = models.CharField(
        max_length=500, verbose_name='Prepend Image URL', default='', blank=True)
    prepend_news_url = models.CharField(
        max_length=500, verbose_name='Prepend News URL', default='', blank=True)

    async def scrape(self, async_client, scraped_articles, failed_websites):
        try:
            print(f'scraping {self.general_name}')
            async with async_client.get(self.website_url, headers=headers) as response:
                response_text = await response.text()

                articles = myscrape.scraper(
                    website_text=response_text,
                    website_name=self.general_name,
                    favicon=self.website_favicon,
                    smallest_article_element=self.smallest_article_element,
                    class_of_smallest_article_element=self.class_of_smallest_article_element or None,
                    smallest_title_element=self.smallest_title_element,
                    class_of_smallest_title_element=self.class_of_smallest_title_element or None,
                    smallest_image_element=self.smallest_image_element,
                    class_of_smallest_image_element=self.class_of_smallest_image_element or None,
                    image_holder_attr=self.image_holder_attr,
                    smallest_link_element_with_class=self.smallest_link_element,
                    class_of_smallest_link_element=self.class_of_smallest_link_element or None,
                    prepend_image_url=self.preprend_image_url,
                    prepend_url=self.prepend_news_url,
                    website_object = self,
                )

                scraped_articles.extend(articles)
                return articles

        except Exception as e:
            print(f'Error ocurred while scraping {self.general_name}:', e)

    def generate_metadata(self):
        return {
            'website': self.general_name,
            'favicon': self.website_favicon,
        }

    def __str__(self) -> str:
        return f'{self.general_name} - {self.sub_category}'


class News(models.Model):
    title = models.CharField(max_length=500)
    url = models.URLField(unique=True)
    img = models.URLField(
        default='https://media.istockphoto.com/vectors/news-vector-id918880270?k=20&m=918880270&s=612x612&w=0&h=bDcgr9jhiRYCPMUhVdLKD5ouIc5daM4qMcaPPapppQI=')
    read_count = models.BigIntegerField(default=0)
    time_added = models.DateTimeField(auto_now_add=True)
    text_content = models.TextField(default='', blank=True)
    website = models.ForeignKey(
        to=Website, related_name='news', on_delete=models.DO_NOTHING, null=True, blank=True)

    entities = models.TextField(default='', blank=True)
    """ 
    the entities field is used by the machine learning model, entities is basically a big string separated by commas - to denote different entities
    """

    def __str__(self):
        return self.title + ' (' + str(self.read_count) + ' reads)'

    def serialize(self):
        website_metadata = self.website.generate_metadata()
        website_metadata['time_added'] = self.time_added
        return {'title': self.title, 'url': self.url, 'img': self.img, 'reads': self.read_count, 'metadata': website_metadata}
