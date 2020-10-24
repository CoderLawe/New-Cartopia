from django.db import models
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
import requests

#source = requests.get("https://www.caranddriver.com/reviews/").text
#soup = BeautifulSoup(source, 'lxml')


# Create your models here.
class Article(models.Model):
    manufacturer = models.CharField(max_length=200)
    carmodel = models.CharField(max_length=200)
    slug = models.SlugField()
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    thumb = models.ImageField( blank = True )
    author = models.ForeignKey(User,on_delete= models.CASCADE,related_name='blog_posts',default='')

    def __str__(self):
        return self.manufacturer +'-' + self.carmodel

    def snippet(self):
        return self.body[:50] + '...'


def tickle(request):
    for article in soup.find_all('div', class_='full-item'):
        headline = article.find('a', class_='full-item-title item-title').text


class Comments(models.Model):
    article = models.ForeignKey(Article,on_delete=models.CASCADE,related_name='comments',null =True)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length = 200)
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return self.name