import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "keep_fm.settings")

app = Celery("keep_fm")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
