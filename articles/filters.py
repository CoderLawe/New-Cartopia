import django_filters
from .models import *



class CommentsFilter(django_filters.FilterSet):
	class Meta:
		model = Comments
		fields = '__all__'
		#exclude = ['customer', 'date_created']