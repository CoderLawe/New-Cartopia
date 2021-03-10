from django.views.generic import View, TemplateView, CreateView, FormView, DetailView, ListView
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .filters import CommentsFilter
from django.db.models import Q




from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Comments, Admin, Newsletter, Carousel
from . import forms
from bs4 import BeautifulSoup
import requests
import csv




# source = requests.get("https://www.caranddriver.com/reviews/").text


class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("admin_login")
        return super().dispatch(request, *args, **kwargs)


class AdminLoginView(FormView):
    template_name = "adminpages/adminlogin.html"   
    form_class = forms.CustomerLoginForm
    success_url = reverse_lazy("admin_home")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Admin.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})
        return super().form_valid(form)


class AdminHomeView(AdminRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        comments = Comments.objects.all()
        articles = Article.objects.all()
        total_articles = articles.count()
        total_comments = comments.count()
        newsletter = Newsletter.objects.all()


        #views_page = articles.page_views
        context = {
            'comments':comments,'articles':articles,'total_articles':total_articles,'total_comments':total_comments,'newsletter':newsletter
        }
        return render(request, "adminpages/admin-home.html", context)

class CommentModeration(AdminRequiredMixin,View):
    def get(self,request, *args, **kwargs):
        comment = Comments.objects.all().order_by('created_on')
        active_comments = comment.filter(active=False)
        comments_filter = CommentsFilter(request.GET, queryset=comment) 
        comment = comments_filter.qs



        context = {
            'comment':comment,
            'active_comments':active_comments,
            'filter':comments_filter

        }

        return render(request,'adminpages/admin_comments.html',context)






"""class CommentDetails(AdminRequiredMixin,View):
    def get(self,request, pk, *args, **kwargs):
        comment_detail = Comments.objects.get(id=pk)

        context = {
            'comment':comment_detail

        }

        return render(request,'adminpages/comments_edit.html',context)
"""
def comment_details(request, pk):
    comments  = Comments.objects.get(id=pk)
    form = forms.ModerateComments(instance=comments)
    

    if request.method == 'POST':
        form = forms.ModerateComments(request.POST, instance=comments)
        if form.is_valid():
            form.save()
            return redirect('admin_home')

    return render(request, 'adminpages/comments_edit.html', {'form': form,'comments':comments})

def article_list(request):
    articles = Article.objects.all().order_by('date')#[0:20]
    carousel_info = Carousel.objects.filter(purpose="Homepage")

    #num_visits = request.session.get('num_visits', 0)
    #request.session['num_visits'] = num_visits + 1

    return render(request, 'articles/article_list.html', {'articles': articles,'carousel_info':carousel_info})



class view_customer(AdminRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        count = num_list
        context = {
            'count':count
        }
        return render(request, "adminpages/chart.html", context)
def article_detail(request, slug):
    # return HttpResponse(slug)
    # article = Article.objects.get(slug=slug)

    template_name = 'post_detail.html'
    articles = get_object_or_404(Article, slug=slug)
    articles.page_views = articles.page_views+1
    articles.save()
    comments = articles.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = forms.CreateComment(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.article = articles
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = forms.CreateComment()

    return render(request, 'articles/article_detail.html', {'article': articles, 'comments': comments,
                                                            'new_comment': new_comment,
                                                            'comment_form': comment_form, 'views':articles.page_views})


def article_create(request):
    context = {} 
    if request.method == "POST": 
        form2 = forms.CreateArticle(request.POST, request.FILES)
       
        if form2.is_valid():
            instance = form2.save(commit = False)
            instance.author = request.user
            instance.save()
            return redirect('list')
         
            
    else: 
        form2 = forms.CreateArticle()
    context['form2']= form2

    return render(request, "adminpages/article_create.html", context) 



class all_articles(AdminRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        article = Article.objects.all()
        context = {
            'articles':article
        }
        return render(request, "adminpages/all_articles.html", context)


def update_article(request,pk):
    article = Article.objects.get(id=pk)
    form= forms.UpdateArticle(instance=article)

    if request.method == 'POST':
        form = forms.UpdateArticle(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    return render(request, 'adminpages/update_article.html', {'form': form,'article':article})


def delete_article(request, pk):
    article = Article.objects.get(id=pk)
    if request.method == "POST":
        article.delete()
        return redirect('admin_home')

    context = {'item': article}
    return render(request, 'adminpages/delete.html', context)

def delete_comment(request, pk):
    comment = comment.objects.get(id=pk)
    if request.method == "POST":
        comment.delete()
        return redirect('admin_home')

    context = {'item': comment}
    return render(request, 'adminpages/delete.html', context)


def update_title(request,pk):
    carousel = Carousel.objects.get(id=pk)
    form= forms.Update_title(instance=carousel)

    if request.method == 'POST':
        form = forms.Update_title(request.POST, instance=carousel)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    return render(request, 'adminpages/update_article.html', {'form': form,'carousel':carousel})

def Export(request):
    
   response = HttpResponse(content_type ='text/csv')

   writer = csv.writer(response)
   writer.writerow(['customer','email'])


   for newsletter in Newsletter.objects.all().values_list('name','email'):

        writer.writerow(newsletter)
       # print (newsletter.name)
   response['content-Disposition'] = 'attachment; filename="Newsletter_signees.csv"'

   return response

def aboutus(request):

    context = {

    }

    return render(request,'articles/aboutus.html',context)


def newsletter_signup(request):
    context = {} 
    if request.method == "POST": 
        form = forms.NewsletterForm(request.POST)
       
        if form.is_valid():
            instance = form.save(commit = False)
            instance.save()
            return redirect('list')
         
            
    else: 
        form = forms.NewsletterForm()
    context['form']= form

    return render(request, "articles/newsletter_signup.html", context) 


def Search(request):
  

    kw = request.GET.get("keyword")
    results = Article.objects.filter(
        Q(body__icontains=kw) | Q(manufacturer__icontains=kw))
    print(results)

    return render(request, 'articles/search.html', {'results': results})

    

def Popup(request):

    context = {} 
    if request.method == "POST": 
        form = forms.NewsletterForm(request.POST)
       
        if form.is_valid():
            instance = form.save(commit = False)
            instance.save()
            return redirect('list')
         
            
    else: 
        form = forms.NewsletterForm()
    context['form']= form

    return render(request,'articles/index.html',context)

    



