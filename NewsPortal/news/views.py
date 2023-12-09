from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView,  CreateView, UpdateView, DeleteView, TemplateView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='Authors').exists()
        return context

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

    def get_template_names(self):
        if self.request.path=='/news/articles/create/':
            self.template_name='articles_create.html'
        else:
            self.template_name='news_create.html'
        return self.template_name

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path== '/news/articles/create/':
            post.choice_field = 'article'
            post.save()
        return super().form_valid(form)

class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def get_template_names(self):
        if self.request.path==f'/news/articles/{self.object.pk}/edit/':
            self.template_name='articles_edit.html'
        else:
            self.template_name='news_edit.html'
        return self.template_name

    class ProtectedView(LoginRequiredMixin, TemplateView):
        template_name = 'protected_page.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')
    context_object_name = 'post'

    def get_template_names(self):
        if self.request.path==f'/news/articles/{self.object.pk}/delete/':
            self.template_name='articles_delete.html'
        else:
            self.template_name='news_delete.html'
        return self.template_name


