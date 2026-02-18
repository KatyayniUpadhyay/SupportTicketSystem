from django.urls import path
from tickets.http_views.ticket_view import TicketView

urlpatterns = [
    path('tickets/', TicketView.as_view(), name='ticket-list-create'),
]
