from django_filters import FilterSet, DateFilter
from .models import Post
from django import forms


class PostFilter(FilterSet):
    creation_date = DateFilter(
        field_name='creation_date',
        widget=forms.DateInput(attrs={'type': 'date'}),
        lookup_expr='date__gte',
    )


class Meta:
    model = Post
    fields = {
        'header': ['icontains'],
        'user': ['exact'],
        'creation_date': ['gt']
    }
