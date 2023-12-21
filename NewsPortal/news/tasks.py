from celery import shared_task
import datetime
from .models import Post
from .models import Category
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string

@shared_task
def info_after_new_post(pk):
    post=Post.objects.get(pk=pk)
    categories=post.category.all()
    header=post.header
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

