from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post
from .filters import PostFilter

class PostList(ListView):
    model=Post
    ordering='-creation_date'
    template_name='posts.html'
    context_object_name ='posts'
    paginate_by = 10


    def get_template_names(self):
        if self.request.path =='/news/':
            self.template_name='posts.html'
        elif self.request.path == '/news/search/':
            self.template_name = 'search.html'
        return self.template_name


    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'specific_post.html'
    context_object_name = 'post'



