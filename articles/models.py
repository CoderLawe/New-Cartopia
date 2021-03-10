from django.db import models
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import requests

#source = requests.get("https://www.caranddriver.com/reviews/").text
#soup = BeautifulSoup(source, 'lxml')


# Create your models here.

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    image = models.ImageField()
    mobile = models.CharField(max_length=20)
    
class Article(models.Model):
    manufacturer = models.CharField(max_length=200)
    carmodel = models.CharField(max_length=200)
    slug = models.SlugField()
    body = RichTextField(blank = True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    thumb = models.ImageField(null=True, blank = True,upload_to = 'images/')
    #image = models.ImageField(default = 'default.png',blank= True)
    author = models.ForeignKey(User,on_delete= models.CASCADE,related_name='blog_posts',default='')
    page_views = models.IntegerField(default=0)

    def __str__(self):
        return self.manufacturer +'-' + self.carmodel

    def snippet(self):
        return self.body[:100] + '...'

    def get_photo_url(self):
        if self.thumb and hasattr(self.thumb, 'url'):
            return self.thumb.url
        else:
            return "/assets/media/default.png"

class Newsletter(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name




def tickle(request):
    for article in soup.find_all('div', class_='full-item'):
        headline = article.find('a', class_='full-item-title item-title').text


class Comments(models.Model):
    article = models.ForeignKey(Article,on_delete=models.CASCADE,related_name='comments',null=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length = 200)
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']   

    def __str__(self):
        return self.name

    def snippet(self):
        return self.comment[:50] + '...'


class Carousel(models.Model):
    title = models.CharField(max_length=200)
    body = RichTextField(blank = True, null=True)
    image = models.ImageField(null=True, blank = True,upload_to = 'images/')
    purpose = models.CharField(max_length=200, default="unlisted")
  #  author = models.ForeignKey(Admin,on_delete= models.CASCADE,related_name='carousel_posts',default='')


   # by = models.ForeignKey(User,on_delete= models.CASCADE,default='')

    

    def __str__(self):
        return self.title




