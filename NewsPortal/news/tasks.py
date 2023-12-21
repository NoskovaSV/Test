from celery import shared_task
from .models import Category
from  import instance


@shared_task
def notify_about_new_post():
    if kwargs['action']=='post_add':
        categories=instance.categories.all()
        subscribers_emails=[]

        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_emails+=[s.email for s in subscribers]


