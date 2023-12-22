import logging
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
import datetime
from news.models import Post
from news.models import Category
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone

logger = logging.getLogger(__name__)


def my_job():
    today = timezone.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(creation_date__gte=last_week)
    categories = set(posts.values_list('categories__category_name', flat=True))
    subscribers = set(
        Category.objects.filter(category_name__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject="Статьи за неделю",
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,

    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="mon", hour="21", minute="00", timezone=settings.TIME_ZONE),

            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="21", minute="00"
            ),

            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

def notifications_on_monday():
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


def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

    # добавляем работу нашему задачнику
    scheduler.add_job(
    notifications_on_monday,
    trigger=CronTrigger(day_of_week="mon", hour="08", minute="00", timezone=settings.TIME_ZONE),
    id="notifications_on_monday ",
    max_instances=1,
    replace_existing=True,
)
logger.info("Added job 'notifications_on_monday'.")

    scheduler.add_job(
    delete_old_job_executions,
    trigger=CronTrigger(
        day_of_week="mon", hour="08", minute="00"
    ),
    id="delete_old_job_executions",
    max_instances=1,
    replace_existing=True,
)
logger.info(
    "Added weekly job: 'delete_old_job_executions'."
)

try:
    logger.info("Starting scheduler...")
    scheduler.start()
except KeyboardInterrupt:
    logger.info("Stopping scheduler...")
    scheduler.shutdown()
    logger.info("Scheduler shut down successfully!")
