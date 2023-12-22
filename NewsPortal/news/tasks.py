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
def notifications_on_Monday (preview, pk,title, subscribers):
    html_content= render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}/'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

    @receiver(m2m_changed, sender=PostCategory)
    def notify_about_new_post(sender, instance, **kwargs):
        if kwargs['action'] == 'post_add':
            categories = instance.categories.all()
            subscribers_emails = []

            for cat in categories:
                subscribers = cat.subscribers.all()
                subscribers_emails += [s.email for s in subscribers]

            notifications_on_Monday(instance.preview(), instance.pk, instance.header, subscribers_emails)