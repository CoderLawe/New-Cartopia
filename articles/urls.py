"""cartopia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.article_list, name='list'),
    path('create/', views.article_create, name='create'),
    #Admin Page Urls
    path('admin-login/',views.AdminLoginView.as_view(), name='admin_login'),
    path('admin-home/',views.AdminHomeView.as_view(),name = 'admin_home'),

    path('update_article/<str:pk>/', views.update_article, name="update_article"),
    path('delete_article/<str:pk>/', views.delete_article, name="delete_article"),
    path('update_title/<str:pk>/', views.update_title, name="update_title"),
    path('popup/', views.Popup, name = "popup"),




    path('admin_edit/<str:pk>/', views.comment_details, name="edit"),
    path('delete_comment/<str:pk>/', views.delete_comment, name="delete_comment"),


    path('admin-comments/',views.CommentModeration.as_view(),name = 'moderate'),
    path('admin-articles/',views.all_articles.as_view(), name='admin_articles'),

    path('export/', views.Export, name="export"),

    path('about/', views.aboutus, name="about"),

    path('newsletter_signup/', views.newsletter_signup, name="newsletter"),

    path('search/', views.Search, name="search"),






   # path('article_detail/<str:pk>/', views.article_detail, name="detail"),

    re_path(r'^(?P<slug>[\w-]+)/$', views.article_detail, name='detail'),



    

]
