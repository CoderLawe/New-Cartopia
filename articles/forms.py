from django import forms
from . import models

class CreateArticle(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = ['manufacturer','carmodel','body','slug','thumb','author']


class CreateComment(forms.ModelForm):
    class Meta:
        model = models.Comments
        fields = ['name','email','comment']


