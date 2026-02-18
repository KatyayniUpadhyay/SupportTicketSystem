
from django.db import models

class Ticket(models.Model):

    class TicketCategory(models.TextChoices):
        BILLING = "billing", "Billing"
        TECHNICAL = "technical", "Technical"
        ACCOUNT = "account", "Account"
        GENERAL = "general", "General"

    class TicketPriority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        CRITICAL = "critical", "Critical"

    class TicketStatus(models.TextChoices):
        OPEN = "open", "Open"
        IN_PROGRESS = "in_progress", "In Progress"
        RESOLVED = "resolved", "Resolved"
        CLOSED = "closed", "Closed"

    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)

    category = models.CharField(
        max_length=250,
        choices=TicketCategory.choices
    )

    priority = models.CharField(
        max_length=250,
        choices=TicketPriority.choices
    )

    status = models.CharField(
        max_length=250,
        choices=TicketStatus.choices,
        default=TicketStatus.OPEN
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = "ticket"

    def __str__(self):
        return self.title

