
from django.db import models
from django.conf import settings


class ItemReport(models.Model):

    class ReportType(models.TextChoices):
        LOST = 'LOST', 'Lost'
        FOUND = 'FOUND', 'Found'

    class Category(models.TextChoices):
        ELECTRONICS = 'ELECTRONICS', 'Electronics'
        BAGS = 'BAGS', 'Bags'
        DOCUMENTS = 'DOCUMENTS', 'Documents'
        CLOTHING = 'CLOTHING', 'Clothing'
        ACCESSORIES = 'ACCESSORIES', 'Accessories'
        JEWELLERY = 'JEWELLERY', 'Jewellery'
        OTHER = 'OTHER', 'Other'

    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        MATCHED = 'MATCHED', 'Matched'
        RECOVERED = 'RECOVERED', 'Recovered'
        CLOSED = 'CLOSED', 'Closed'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='item_reports'
    )

    report_type = models.CharField(
        max_length=5,
        choices=ReportType.choices
    )

    item_name = models.CharField(max_length=150)
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.OTHER
    )

    description = models.TextField()
    brand = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=50, blank=True)

    image = models.ImageField(
        upload_to='item_reports/',
        blank=True,
        null=True
    )

    location = models.CharField(max_length=255)
    city = models.CharField(max_length=100)

    occurred_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the item was lost or found"
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['report_type', 'status']),
            models.Index(fields=['category', 'city']),
        ]

    def __str__(self):
        return f"{self.get_report_type_display()}: {self.item_name}"
        

class RecoveryRequest(models.Model):

    class RequestStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        REJECTED = 'REJECTED', 'Rejected'
        CANCELLED = 'CANCELLED', 'Cancelled'

    lost_report = models.ForeignKey(
        ItemReport,
        on_delete=models.CASCADE,
        related_name='recovery_requests'
    )

    found_report = models.ForeignKey(
        ItemReport,
        on_delete=models.CASCADE,
        related_name='recovery_claims'
    )

    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_recovery_requests'
    )

    message = models.TextField(
        help_text="Explain why you believe this is your item"
    )

    status = models.CharField(
        max_length=10,
        choices=RequestStatus.choices,
        default=RequestStatus.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['lost_report', 'found_report', 'requester'],
                name='unique_recovery_request'
            )
        ]

    def __str__(self):
        return f"Recovery request #{self.id} - {self.status}"

class ItemMatch(models.Model):
    lost_report = models.ForeignKey(
        ItemReport,
        on_delete=models.CASCADE,
        related_name='lost_matches'
    )
    found_report = models.ForeignKey(
        ItemReport,
        on_delete=models.CASCADE,
        related_name='found_matches'
    )
    score = models.FloatField()
    reasons = models.JSONField(default=list)
    is_notified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('lost_report', 'found_report')
        ordering = ['-score']

    def __str__(self):
        return f"Match: {self.lost_report.item_name} - {self.found_report.item_name}"