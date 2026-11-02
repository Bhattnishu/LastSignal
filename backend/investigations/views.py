
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from items.models import ItemReport
from .models import Investigation, TimelineEntry, InvestigationSuggestion
from .serializers import (
    SuggestionUpdateSerializer,
    InvestigationUpdateSerializer,
    InvestigationSerializer,
    InvestigationSuggestionSerializer,
    TimelineEntrySerializer,
)


class InvestigationCreateView(generics.CreateAPIView):
    serializer_class = InvestigationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        lost_report = get_object_or_404(
            ItemReport,
            id=self.request.data.get('lost_report'),
            user=self.request.user,
            report_type=ItemReport.ReportType.LOST
        )

        if Investigation.objects.filter(lost_report=lost_report).exists():
            raise ValidationError(
                "An investigation already exists for this item."
            )

        serializer.save(
            lost_report=lost_report,
            user=self.request.user
        )


class TimelineEntryCreateView(generics.CreateAPIView):
    serializer_class = TimelineEntrySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        investigation = get_object_or_404(
            Investigation,
            id=self.request.data.get('investigation'),
            user=self.request.user
        )

        if investigation.status != Investigation.InvestigationStatus.ACTIVE:
            raise ValidationError("This investigation is not active.")

        serializer.save(investigation=investigation)


class MyTimelineView(generics.ListAPIView):
    serializer_class = TimelineEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TimelineEntry.objects.filter(
            investigation__user=self.request.user
        ).select_related('investigation')


class InvestigationSuggestionCreateView(generics.CreateAPIView):
    serializer_class = InvestigationSuggestionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        investigation = get_object_or_404(
            Investigation,
            id=self.request.data.get('investigation'),
            user=self.request.user
        )

        if investigation.status != Investigation.InvestigationStatus.ACTIVE:
            raise ValidationError("This investigation is not active.")

        serializer.save(investigation=investigation)


class MySuggestionsView(generics.ListAPIView):
    serializer_class = InvestigationSuggestionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InvestigationSuggestion.objects.filter(
            investigation__user=self.request.user
        ).select_related('investigation')


class InvestigationUpdateView(generics.UpdateAPIView):
    serializer_class = InvestigationUpdateSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch']

    def get_queryset(self):
        return Investigation.objects.filter(
            user=self.request.user,
            status=Investigation.InvestigationStatus.ACTIVE
        )


class SuggestionUpdateView(generics.UpdateAPIView):
    serializer_class = SuggestionUpdateSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch']

    def get_queryset(self):
        return InvestigationSuggestion.objects.filter(
            investigation__user=self.request.user,
            investigation__status=Investigation.InvestigationStatus.ACTIVE
        )
