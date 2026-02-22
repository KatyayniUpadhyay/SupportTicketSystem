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

    # 🔹 NEW METHOD (needed for status progression)
    @staticmethod
    def get_ticket_by_id(ticket_id: int) -> Ticket | None:
        """
        Returns a ticket by id or None if not found.
        """
        try:
            return Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            return None

    @staticmethod
    def create_ticket(validated_data: dict) -> Ticket:
        """
        Creates a ticket instance using validated serializer data.
        """
        ticket = Ticket.objects.create(**validated_data)
        return ticket

    @staticmethod
    def update_ticket(ticket_id: int, validated_data: dict) -> Ticket:
        """
        Business logic for updating ticket.
        """

        ticket = get_object_or_404(Ticket, id=ticket_id)

        # 🔹 Business rule: Prevent reopening closed ticket
        if (
            ticket.status == Ticket.TicketStatus.CLOSED
            and validated_data.get("status") == Ticket.TicketStatus.OPEN
        ):
            raise ValueError("Closed tickets cannot be reopened.")

        for field, value in validated_data.items():
            setattr(ticket, field, value)

        ticket.save()
        return ticket

    # 🔹 NEW METHOD (clean auto status progression)
    @staticmethod
    def progress_ticket_status(ticket_id: int) -> Ticket:
        """
        Auto-progress ticket status:
        open → in_progress → resolved → closed
        """

        ticket = get_object_or_404(Ticket, id=ticket_id)

        status_flow = {
            Ticket.TicketStatus.OPEN: Ticket.TicketStatus.IN_PROGRESS,
            Ticket.TicketStatus.IN_PROGRESS: Ticket.TicketStatus.RESOLVED,
            Ticket.TicketStatus.RESOLVED: Ticket.TicketStatus.CLOSED,
            Ticket.TicketStatus.CLOSED: Ticket.TicketStatus.CLOSED,
        }

        ticket.status = status_flow.get(ticket.status, Ticket.TicketStatus.CLOSED)
        ticket.save()

        return ticket
