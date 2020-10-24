from django.contrib import admin

# Register your models here.
from .models import Article, Comments

admin.site.register(Article)
admin.site.register(Comments)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'comment', 'article', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'comment')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)