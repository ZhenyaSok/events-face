from django.db import models

import uuid
from django.db import models


class Venue(models.Model):
    """
    Площадка (место проведения события)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("Название", max_length=255)

    class Meta:
        verbose_name = "Площадка"
        verbose_name_plural = "Площадки"

    def __str__(self):
        return self.name


class Event(models.Model):
    """
    Мероприятие
    """
    class Status(models.TextChoices):
        OPEN = "open", "Открыто"
        CLOSED = "closed", "Закрыто"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("Название", max_length=255)
    date = models.DateTimeField("Дата проведения")
    status = models.CharField(
        "Статус",
        max_length=10,
        choices=Status.choices,
        default=Status.OPEN,
    )
    venue = models.ForeignKey(
        Venue,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events",
        verbose_name="Площадка",
    )

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"
