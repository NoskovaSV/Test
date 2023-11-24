from django.shortcuts import render
from django.views.generic import ListView
from .models import Post

class PostList(ListView):
    model=Post
    ordering='choice_field'
    template_name='default.html'
    context_object_name ='posts'



