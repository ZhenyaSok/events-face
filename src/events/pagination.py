from rest_framework.pagination import CursorPagination


class EventCursorPagination(CursorPagination):
    page_size = 10  # сколько элементов на странице
    ordering = "date"  # поле, по которому будет курсор (можно менять на '-date' для обратного порядка)
    cursor_query_param = "cursor"  # параметр в URL, например ?cursor=abc123
