from django.db.models import Count
from django.db.models.functions import TruncDate
from django.db.models import Avg

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from tickets.model_classes.ticket import Ticket


class TicketsStatsView(APIView):

    def get(self, request):
        # Total tickets
        total_tickets = Ticket.objects.count()

        # Open tickets
        open_tickets = Ticket.objects.filter(
            status=Ticket.TicketStatus.OPEN
        ).count()

        # Average tickets per day
        daily_counts = (
            Ticket.objects
            .annotate(day=TruncDate("created_at"))
            .values("day")
            .annotate(count=Count("id"))
        )

        avg_tickets_per_day = (
            daily_counts.aggregate(avg=Avg("count"))["avg"]
            if total_tickets > 0 else 0
        )

        # Priority breakdown
        priority_data = (
            Ticket.objects
            .values("priority")
            .annotate(count=Count("id"))
        )

        priority_breakdown = {
            item["priority"]: item["count"]
            for item in priority_data
        }

        # Category breakdown
        category_data = (
            Ticket.objects
            .values("category")
            .annotate(count=Count("id"))
        )

        category_breakdown = {
            item["category"]: item["count"]
            for item in category_data
        }

        response_data = {
            "total_tickets": total_tickets,
            "open_tickets": open_tickets,
            "avg_tickets_per_day": round(avg_tickets_per_day or 0, 2),
            "priority_breakdown": priority_breakdown,
            "category_breakdown": category_breakdown,
        }

        return Response(response_data, status=status.HTTP_200_OK)
