# from django.shortcuts import render
#
# from rest_framework import viewsets, filters
# from django_filters.rest_framework import DjangoFilterBackend
# from .models import Event
# from .serializers import EventSerializer
#
#
# class EventViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     Список мероприятий (только open), с фильтрацией, сортировкой и пагинацией.
#     """
#     serializer_class = EventSerializer
#     filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
#     filterset_fields = ["name"]  # фильтрация по названию
#     search_fields = ["name"]     # поиск по названию (LIKE)
#     ordering_fields = ["date"]   # сортировка по дате
#     ordering = ["date"]          # сортировка по умолчанию
#
#     def get_queryset(self):
#         return (
#             Event.objects
#             .filter(status=Event.Status.OPEN)
#             .select_related("venue")  # решает проблему N+1
#         )
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Event
from .serializers import EventSerializer
from .pagination import EventCursorPagination


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ["name"]      # фильтрация по названию
    search_fields = ["name"]         # поиск по названию
    ordering_fields = ["date"]       # сортировка по дате
    ordering = ["date"]              # сортировка по умолчанию
    pagination_class = EventCursorPagination  # подключаем курсорную пагинацию

    def get_queryset(self):
        return (
            Event.objects
            .filter(status=Event.Status.OPEN)
            .select_related("venue")  # предотвращаем N+1
        )

