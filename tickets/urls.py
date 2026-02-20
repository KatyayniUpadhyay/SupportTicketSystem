from django.urls import path
from tickets.http_views.ticket_view import TicketView
from tickets.http_views.tickets_stats_view import TicketsStatsView
from tickets.http_views.ticket_classify_view import TicketClassifyView

urlpatterns = [
    path('tickets/', TicketView.as_view(), name='ticket-list-create'),
    path('tickets/classify/', TicketClassifyView.as_view(), name='ticket-classify'),
    path('tickets/<int:id>/', TicketView.as_view(), name='ticket-update'),
    path('tickets/stats/', TicketsStatsView.as_view(), name='ticket-stats'),
]
