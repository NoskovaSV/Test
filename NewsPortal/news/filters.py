from django_filters import FilterSet, DateFilter, CharFilter, ModelChoiceFilter
from .models import Author
from django import forms


class PostFilter(FilterSet):
    creation_date = DateFilter(
        field_name='creation_date',
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дата позже',
        lookup_expr='date__gte',
    )

    header=CharFilter(
        field_name='header',
        label='Заголовок',
        lookup_expr='iregex'
    )
    user=ModelChoiceFilter(
        empty_label='Все авторы',
        field_name='user',
        label='Автор',
        queryset=Author.objects.all()

    )