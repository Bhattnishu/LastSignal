
from django.db import models
from django.conf import settings


class Investigation(models.Model):

    class InvestigationStatus(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        COMPLETED = 'COMPLETED', 'Completed'
        CLOSED = 'CLOSED', 'Closed'

    lost_report = models.OneToOneField(
        'items.ItemReport',
        on_delete=models.CASCADE,
        related_name='investigation'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='investigations'
    )

    status = models.CharField(
        max_length=10,
        choices=InvestigationStatus.choices,
        default=InvestigationStatus.ACTIVE
    )

    ai_summary = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Investigation for {self.lost_report.item_name}"


class TimelineEntry(models.Model):

    investigation = models.ForeignKey(
        Investigation,
        on_delete=models.CASCADE,
        related_name='timeline_entries'
    )

    place = models.CharField(max_length=255)

    description = models.TextField(
        blank=True,
        help_text="What happened at this place?"
    )

    visited_at = models.DateTimeField(
        null=True,
        blank=True
    )

    sequence = models.PositiveIntegerField(
        default=0,
        help_text="Order of this entry in the journey"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sequence', 'visited_at']

    def __str__(self):
        return f"{self.place} - {self.investigation.lost_report.item_name}"


class InvestigationSuggestion(models.Model):

    class SuggestionType(models.TextChoices):
        PLACE = 'PLACE', 'Place to Check'
        ACTION = 'ACTION', 'Action to Take'
        QUESTION = 'QUESTION', 'Follow-up Question'

    investigation = models.ForeignKey(
        Investigation,
        on_delete=models.CASCADE,
        related_name='suggestions'
    )

    suggestion_type = models.CharField(
        max_length=10,
        choices=SuggestionType.choices
    )

    title = models.CharField(max_length=200)

    description = models.TextField()

    reason = models.TextField(
        blank=True,
        help_text="Why is this suggestion relevant?"
    )

    is_completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.investigation.lost_report.item_name}"
