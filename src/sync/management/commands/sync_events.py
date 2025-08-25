import requests
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from events.models import Event, Venue
from sync.models import SyncLog
from django.utils.dateparse import parse_datetime

API_URL = "https://events.k3scluster.tech/api/events/"

class Command(BaseCommand):
    help = "Синхронизация мероприятий с events-provider"

    def add_arguments(self, parser):
        parser.add_argument(
            "--date",
            type=str,
            help="Дата для синхронизации в формате YYYY-MM-DD"
        )
        parser.add_argument(
            "--all",
            action="store_true",
            help="Синхронизировать абсолютно все мероприятия"
        )

    def handle(self, *args, **options):
        sync_date = options.get("date")
        sync_all = options.get("all", False)

        if sync_all:
            url = API_URL
        else:
            if not sync_date:
                yesterday = date.today() - timedelta(days=1)
                sync_date = yesterday.isoformat()
            url = f"{API_URL}?changed_at={sync_date}"

        self.stdout.write(f"Fetching events from: {url}")
        response = requests.get(url)
        if response.status_code != 200:
            self.stderr.write(f"Failed to fetch events: {response.status_code}")
            return

        events_data = response.json()
        new_count = 0
        updated_count = 0

        for item in events_data:
            # Площадка
            venue_data = item.get("venue")
            if venue_data:
                venue, _ = Venue.objects.get_or_create(name=venue_data["name"])
            else:
                venue = None

            # Ивент
            event_obj, created = Event.objects.update_or_create(
                id=item["id"],  # предполагается, что id совпадает
                defaults={
                    "name": item["name"],
                    "date": parse_datetime(item["date"]),
                    "status": item.get("status", "open"),
                    "venue": venue
                }
            )
            if created:
                new_count += 1
            else:
                updated_count += 1

        # Логируем результат
        SyncLog.objects.create(
            sync_date=sync_date,
            new_events_count=new_count,
            updated_events_count=updated_count
        )

        self.stdout.write(self.style.SUCCESS(
            f"Synchronization finished. New: {new_count}, Updated: {updated_count}"
        ))
