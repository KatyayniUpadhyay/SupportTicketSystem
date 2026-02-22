from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.db.models import Q

from tickets.forms.ticket_serializer import TicketSerializer
from tickets.helper_classes.ticket_helper import TicketHelper
from tickets.model_classes.ticket import Ticket


class TicketView(APIView):

    def get(self, request):
        """
        Fetch all tickets with optional search + filters.
        """

        queryset = TicketHelper.get_all_tickets()

        # ----------------------
        # SEARCH
        # ----------------------
        search_query = request.query_params.get("search")

        if search_query and len(search_query) > 3:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        # ----------------------
        # FILTERS
        # ----------------------
        category = request.query_params.get("category")
        priority = request.query_params.get("priority")
        status_param = request.query_params.get("status")

        if category:
            queryset = queryset.filter(category=category)

        if priority:
            queryset = queryset.filter(priority=priority)

        if status_param:
            queryset = queryset.filter(status=status_param)

        queryset = queryset.order_by("-created_at")

        serializer = TicketSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new ticket.
        """
        serializer = TicketSerializer(data=request.data)

        if serializer.is_valid():
            ticket = TicketHelper.create_ticket(serializer.validated_data)
            response_serializer = TicketSerializer(ticket)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        """
        If body contains data → normal update (edit page).
        If body is empty → auto-progress status (row click).
        """

        # 🔹 If frontend sends update data → normal edit flow
        if request.data:
            serializer = TicketSerializer(data=request.data, partial=True)

            if serializer.is_valid():
                try:
                    ticket = TicketHelper.update_ticket(id, serializer.validated_data)
                    return Response(
                        TicketSerializer(ticket).data,
                        status=status.HTTP_200_OK
                    )
                except ValueError as e:
                    return Response(
                        {"error": str(e)},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 🔹 If no body → auto-progress status
        try:
            ticket = TicketHelper.progress_ticket_status(id)
            return Response(
                TicketSerializer(ticket).data,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )