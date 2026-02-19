from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from tickets.forms.ticket_serializer import TicketSerializer
from tickets.helper_classes.ticket_helper import TicketHelper


class TicketView(APIView):

    def get(self, request):
        """
        Fetch all tickets.
        """
        tickets = TicketHelper.get_all_tickets()
        serializer = TicketSerializer(tickets, many=True)
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
        Partially update a ticket
        """
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