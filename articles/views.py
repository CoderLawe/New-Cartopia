from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Comments
from . import forms
from bs4 import BeautifulSoup
import requests


# source = requests.get("https://www.caranddriver.com/reviews/").text

def article_list(request):
    articles = Article.objects.all().order_by('date');
    return render(request, 'articles/article_list.html', {'articles': articles, })


def article_detail(request, slug):
    # return HttpResponse(slug)
    # article = Article.objects.get(slug=slug)

    template_name = 'post_detail.html'
    article = get_object_or_404(Article, slug=slug)
    comments = article.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = forms.CreateComment(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = article
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = forms.CreateComment()

    return render(request, 'articles/article_detail.html', {'article': article, 'comments': comments,
                                                            'new_comment': new_comment,
                                                            'comment_form': comment_form})


def article_create(request):
    if request.method == 'POST':
        form = forms.CreateArticle(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            # instance.author = request.user
            instance.save()
            return redirect('list')

    else:
        form = forms.CreateArticle()
    return render(request, 'articles/article_create.html', {'form': form})




