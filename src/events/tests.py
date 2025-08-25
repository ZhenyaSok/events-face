
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from events.models import Event, Venue
from datetime import datetime, timedelta


@pytest.mark.django_db
class TestEventAPI:
    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def venue(self):
        return Venue.objects.create(name="Главная сцена")

    @pytest.fixture
    def events(self, venue):
        # Создаем несколько мероприятий с разными статусами и датами
        open_event = Event.objects.create(
            name="Открытое событие",
            date=datetime.now(),
            status=Event.Status.OPEN,
            venue=venue
        )
        closed_event = Event.objects.create(
            name="Закрытое событие",
            date=datetime.now() + timedelta(days=1),
            status=Event.Status.CLOSED,
            venue=venue
        )
        return [open_event, closed_event]

    def test_list_open_events(self, client, events):
        url = reverse("event-list")
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        # Проверяем, что возвращается только одно open мероприятие
        assert data["count"] == 1
        assert data["results"][0]["status"] == "open"
        assert data["results"][0]["venue_name"] == "Главная сцена"

    def test_filter_by_name(self, client, events):
        url = reverse("event-list") + "?search=Открытое"
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["count"] == 1
        assert "Открытое" in data["results"][0]["name"]

    def test_ordering_by_date(self, client, venue):
        # создаем несколько мероприятий
        Event.objects.create(name="Event 1", date=datetime(2025,1,1), status=Event.Status.OPEN, venue=venue)
        Event.objects.create(name="Event 2", date=datetime(2025,1,2), status=Event.Status.OPEN, venue=venue)
        url = reverse("event-list") + "?ordering=-date"
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        dates = [e["date"] for e in response.json()["results"]]
        assert dates == sorted(dates, reverse=True)

    def test_pagination_limit(self, client, venue):
        # создаем 15 мероприятий
        for i in range(15):
            Event.objects.create(name=f"Event {i}", date=datetime.now(), status=Event.Status.OPEN, venue=venue)
        url = reverse("event-list")
        response = client.get(url)
        data = response.json()
        # Проверяем, что на странице максимум 10
        assert len(data["results"]) == 10
        assert data["count"] == 15
