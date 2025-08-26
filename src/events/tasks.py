import requests

from celery import shared_task

from .models import Registration


@shared_task(bind=True, soft_time_limit=3600)  # не более 1 часа
def process_registration(self, registration_id):
    try:
        reg = Registration.objects.get(id=registration_id)
        # Здесь логика подтверждения/отказа
        # Для примера просто подтверждаем
        reg.status = Registration.Status.CONFIRMED
        reg.save()

        # Отправка уведомления через notification-service
        notification_payload = {
            "user_id": reg.user.id,
            "event_id": reg.event.id,
            "status": reg.status,
        }
        requests.post(
            "https://notification-service/api/notify/",
            json=notification_payload,
            timeout=5,
        )
    except Exception as e:
        # Логируем ошибки
        print(f"Error processing registration {registration_id}: {e}")
