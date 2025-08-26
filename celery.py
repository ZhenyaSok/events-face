import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "events_face.settings")
app = Celery("events_face")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
