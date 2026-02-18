
from typing import Tuple
from django.db.models import QuerySet

from tickets.model_classes.ticket import Ticket


class TicketHelper:
    """
    Contains all business logic related to Ticket operations.
    Views should call this layer instead of directly interacting with models.
    """

    @staticmethod
    def get_all_tickets() -> QuerySet[Ticket]:
        """
        Returns all tickets ordered by latest created.
        """
        return Ticket.objects.all().order_by("-created_at")

    @staticmethod
    def create_ticket(validated_data: dict) -> Ticket:
        """
        Creates a ticket instance using validated serializer data.
        Business logic (like auto-classification) can be added here later.
        """
        # Future LLM auto-suggestion logic can go here

        ticket = Ticket.objects.create(**validated_data)
        return ticket
