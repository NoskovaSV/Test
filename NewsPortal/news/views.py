from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView,  CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm

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

class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path== '/news/articles/create/':
            post.choice_field = 'A'
            post.save()
        return super().form_valid(form)

class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

class PostDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')


