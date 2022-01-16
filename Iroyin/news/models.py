from operator import mod
from django.db import models

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=500)
    url = models.URLField(unique=True)
    
    def __str__(self):
        return self.title
    
    def serialize(self):
        
        return {'newsId': self.id, 'title': self.title, 'url': self.url }
    

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.TextField(max_length=50)
    newsSeen = models.ManyToManyField(to = News, related_name='readers')
    newsIntereactedWith = models.ManyToManyField(to = News, related_name='readers_interacted')
    
    def __str__(self):
        return self.username
    
