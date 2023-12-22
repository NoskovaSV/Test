from celery import shared_task
import datetime
from .models import Post
from .models import Category
from .models import PostCategory
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils import timezone

@shared_task
def info_after_new_post(pk):
    post=Post.objects.get(pk=pk)
    categories=post.categories.all()
    header=post.header
    preview=post.preview()
    subscribers_emails=[]

    for cat in categories:
        subscribers = cat.subscribers.all()
        subscribers_emails += [s.email for s in subscribers]

        html_content = render_to_string(
            'post_created_email.html',
            {
                'text': preview,
                'link': f'{settings.SITE_URL}/news/{pk}/'
            }
        )

        msg= EmailMultiAlternatives(
        subject=header,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
        msg.attach_alternative(html_content,'text/html')
        msg.send()

@shared_task
def notifications_on_monday (preview, pk,title, subscribers):
    today = timezone.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(creation_date__gte=last_week)
    categories = set(posts.values_list('categories__category_name', flat=True))
    subscribers = set(
        Category.objects.filter(category_name__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'monday_letters.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject="Новые статьи за неделю",
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,

    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

