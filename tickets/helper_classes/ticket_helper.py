
from typing import Tuple
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
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

    @staticmethod
    def update_ticket(ticket_id: int, validated_data: dict) -> Ticket:
        """
        Business logic for updating ticket.
        """
        ticket = get_object_or_404(Ticket, id=ticket_id)

        # Example business rule:
        # Prevent reopening a closed ticket
        if (
                ticket.status == Ticket.TicketStatus.CLOSED
                and validated_data.get("status") == Ticket.TicketStatus.OPEN
        ):
            raise ValueError("Closed tickets cannot be reopened.")

        for field, value in validated_data.items():
            setattr(ticket, field, value)

        ticket.save()
        return ticket
