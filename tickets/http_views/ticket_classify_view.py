import json
import time
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Import Google API exceptions for error handling
from google.api_core import exceptions

from tickets.model_classes.ticket import Ticket
from tickets.helper_classes.LLM_helper import LLMHelper


class TicketClassifyView(APIView):

    def post(self, request):
        description = request.data.get("description")

        if not description:
            return Response(
                {"error": "description is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        allowed_categories = [choice[0] for choice in Ticket.TicketCategory.choices]
        allowed_priorities = [choice[0] for choice in Ticket.TicketPriority.choices]

        # 1. Define the Schema for Gemini 2.5
        response_schema = {
            "type": "OBJECT",
            "properties": {
                "category": {"type": "STRING", "enum": allowed_categories},
                "priority": {"type": "STRING", "enum": allowed_priorities},
            },
            "required": ["category", "priority"]
        }

        prompt = f"""
        Classify this support ticket.
        Description: "{description}"
        """

        # 2. Implementation with Retry Logic for Quota (429)
        max_retries = 3
        wait_time = 2  # Seconds

        for attempt in range(max_retries):
            try:
                client = LLMHelper.get_gemini_model()

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config={
                        "response_mime_type": "application/json",
                        "response_schema": response_schema
                    }
                )

                # Extract and parse
                result = json.loads(response.text)

                return Response({
                    "suggested_category": result.get("category"),
                    "suggested_priority": result.get("priority")
                }, status=status.HTTP_200_OK)

            except exceptions.ResourceExhausted:
                # This is the 429 error
                if attempt < max_retries - 1:
                    time.sleep(wait_time)
                    wait_time *= 2  # Exponential backoff (2s, 4s...)
                    continue
                else:
                    return Response(
                        {"error": "API Quota exhausted. Please wait a minute before retrying."},
                        status=status.HTTP_429_TOO_MANY_REQUESTS
                    )

            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )