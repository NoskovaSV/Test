from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.core.validators import MinValueValidator
from django.urls import reverse

class Author(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rating=self.post.aggregate(pr=Coalesce(Sum("rating"),0)).get("pr")
        comment_rating=self.user.comment.aggregate(cr=Coalesce(Sum("rating"),0)).get("cr")
        post_comment_rating=self.post.aggregate(pcr=Coalesce(Sum("comment__rating"),0)).get("pcr")


        self.rating=post_rating*3+comment_rating+post_comment_rating
        self.save()

    def __str__(self):
        return self.user.username

class Category(models.Model):
    category_name = models.CharField(max_length=255, default="Default value", unique=True)

    def __str__(self):
        return self.category_name.title()

class Post(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="post")
    A = "article"
    N = "news"
    choices = ((A, "Статья")), (N, "Новость")
    choice_field = models.CharField(max_length=7, choices=choices, default="news")
    creation_date = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through="PostCategory")
    header = models.CharField(max_length=255, default="Default value")
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        preview = self.text[124:]
        return preview

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    text = models.TextField()
    comment_date = models.DateField(auto_now_add=True)
    rating = models.IntegerField(default=0)


    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.post.title()}: {self.text[:20]}'
