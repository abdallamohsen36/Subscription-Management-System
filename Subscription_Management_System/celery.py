import os
from celery import Celery

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "Subscription_Management_System.settings"
)

app = Celery("Subscription_Management_System")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()