from django.db import models
from django.utils import timezone


class SyncLog(models.Model):
    """
    Лог синхронизации с events-provider
    """

    sync_date = models.DateField(default=timezone.now)
    new_events_count = models.PositiveIntegerField(default=0)
    updated_events_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Лог синхронизации"
        verbose_name_plural = "Логи синхронизации"

    def __str__(self):
        return f"{self.sync_date}: {self.new_events_count} new, {self.updated_events_count} updated"
