from operator import mod
from django.db import models
from sklearn.metrics import max_error

# Create your models here.

class Interest(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    
class News(models.Model):
    title = models.CharField(max_length=500)
    url = models.URLField(unique=True)
    img = models.URLField(default = 'https://media.istockphoto.com/vectors/news-vector-id918880270?k=20&m=918880270&s=612x612&w=0&h=bDcgr9jhiRYCPMUhVdLKD5ouIc5daM4qMcaPPapppQI=')

    def __str__(self):
        return self.title
    
    def serialize(self):
        
        return {'title': self.title, 'url': self.url, 'img': self.img }
    

class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.TextField(max_length=50)
    newsSeen = models.ManyToManyField(to = News, related_name='readers')
    newInteractedWith = models.ManyToManyField(to = News, related_name='readers_interacted')
    interests = models.ManyToManyField(to = Interest, related_name='users')
    
    def __str__(self):
        return self.username
    