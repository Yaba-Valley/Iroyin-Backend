from django.db import models


class Interest(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Website(models.Model):
    general_name = models.CharField(max_length=500, verbose_name='Name')
    sub_category = models.CharField(max_length=100)
    categories = models.ManyToManyField(to=Interest, related_name='websites')
    website_favicon = models.URLField(
        verbose_name='Favicon', default='https://media.istockphoto.com/vectors/news-vector-id918880270?k=20&m=918880270&s=612x612&w=0&h=bDcgr9jhiRYCPMUhVdLKD5ouIc5daM4qMcaPPapppQI=')
    

    def scrape(self):
        pass

    def generate_metadata(self):
        return {
            'website': self.general_name,
            'favicon': self.website_favicon,
        }


class News(models.Model):
    title = models.CharField(max_length=500)
    url = models.URLField(unique=True)
    img = models.URLField(
        default='https://media.istockphoto.com/vectors/news-vector-id918880270?k=20&m=918880270&s=612x612&w=0&h=bDcgr9jhiRYCPMUhVdLKD5ouIc5daM4qMcaPPapppQI=')
    read_count = models.BigIntegerField(default=0)
    categories = models.ManyToManyField(to=Interest)
    time_added = models.DateTimeField(auto_now_add=True)
    text_content = models.TextField(default='')
    website = models.ForeignKey(to = Website, related_name='news', on_delete=models.RESTRICT)

    # website_name = models.TextField(default='Unknown')
    # website_favicon = models.URLField(
    # default='')
    entities = models.TextField(default='')
    """ 
    the entities field is used by the machine learning model, entities is basically a big string separated by commas - to denote different entities
    """

    def __str__(self):
        return self.title + ' (' + str(self.read_count) + ' reads)'

    def serialize(self):
        website_metadata = self.website.generate_metadata()
        website_metadata['time_added'] = self.time_added
        return {'title': self.title, 'url': self.url, 'img': self.img, 'reads': self.read_count, 'metadata': website_metadata}
