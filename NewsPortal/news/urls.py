from django.urls import path
from .views import PostList, PostDetail, PostCreate

urlpatterns = [
    path('', PostList.as_view()),
    path('search/', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
    path('create/', PostCreate.as_view(), name='news_create'),

]

