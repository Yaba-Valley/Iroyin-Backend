from django.db import models

class Interest(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=500)
    url = models.URLField(unique=True)
    img = models.URLField(
        default='https://media.istockphoto.com/vectors/news-vector-id918880270?k=20&m=918880270&s=612x612&w=0&h=bDcgr9jhiRYCPMUhVdLKD5ouIc5daM4qMcaPPapppQI=')
    read_count = models.BigIntegerField(default=0)
    categories = models.ManyToManyField(to=Interest)
    time_added = models.DateTimeField(auto_now=True)

    website_name = models.TextField(default='Unknown')
    website_favicon = models.URLField(
        default='https://media.istockphoto.com/vectors/news-vector-id918880270?k=20&m=918880270&s=612x612&w=0&h=bDcgr9jhiRYCPMUhVdLKD5ouIc5daM4qMcaPPapppQI=')

    def __str__(self):
        return self.title + ' (' + str(self.read_count) + ' reads)'
    
    def serialize(self):
        return {'title': self.title, 'url': self.url, 'img': self.img, 'metadata': {'website': self.website_name, 'favicon': self.website_favicon}}
