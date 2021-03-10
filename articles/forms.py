from django import forms
from . import models

class CreateArticle(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = ['manufacturer','carmodel','body','slug','thumb','author']

class NewsletterForm(forms.ModelForm):

    class Meta:
        model = models.Newsletter
        fields = ['name','email']


class CreateComment(forms.ModelForm):
    class Meta:
        model = models.Comments
        fields = ['name','email','comment']

class ModerateComments(forms.ModelForm):
    class Meta:
        model = models.Comments
        fields = ['article','name','email','comment','active']

class UpdateArticle(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = '__all__'

"""
class Update_title(forms.ModelForm):
    class Meta:
        model = models.Carousel
        fields = '__all__'
 """
class CustomerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())



class HomeForm(forms.Form): 
   
    geeks_field = forms.ImageField()

class EditProperties(forms.ModelForm):
    class Meta:
        model = models.Carousel
        fields = '__all__'

        exclude = ['purpose']


