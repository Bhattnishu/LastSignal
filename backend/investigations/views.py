
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from items.models import ItemReport
from .models import Investigation, TimelineEntry, InvestigationSuggestion
from .serializers import (
    SuggestionUpdateSerializer,
    InvestigationUpdateSerializer,
    InvestigationSerializer,
    InvestigationSuggestionSerializer,
    TimelineEntrySerializer,
)
from .ai_service import (
    generate_investigation_analysis,
    generate_fallback_analysis,
)


class InvestigationCreateView(generics.GenericAPIView):
    serializer_class = InvestigationSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        lost_report = get_object_or_404(
            ItemReport,
            id=request.data.get('lost_report'),
            user=request.user,
            report_type=ItemReport.ReportType.LOST
        )

        investigation, created = Investigation.objects.get_or_create(
            lost_report=lost_report,
            defaults={"user": request.user}
        )

        serializer = self.get_serializer(investigation)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
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



class AIAnalysisView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        investigation_id = request.data.get("investigation")

        investigation = get_object_or_404(
            Investigation,
            id=investigation_id,
            user=request.user
        )

        if investigation.status != "ACTIVE":
            return Response(
                {"error": "This investigation is not active."},
                status=status.HTTP_400_BAD_REQUEST
            )

        timeline = TimelineEntry.objects.filter(
            investigation=investigation
        ).order_by("sequence", "visited_at")

        timeline_data = [
            {
                "place": entry.place,
                "description": entry.description,
                "visited_at": (
                    entry.visited_at.isoformat()
                    if entry.visited_at else "Not provided"
                )
            }
            for entry in timeline
        ]

        try:
            analysis = generate_investigation_analysis(
                investigation.lost_report,
                timeline_data
            )
            analysis_source = "gemini"

        except Exception as e:
            print("GEMINI ERROR:", repr(e))

            analysis = generate_fallback_analysis(
                investigation.lost_report,
                timeline_data
            )
            analysis_source = "fallback"

        investigation.ai_summary = analysis
        investigation.save(
            update_fields=["ai_summary", "updated_at"]
        )

        return Response({
            "analysis": analysis,
            "source": analysis_source
        })
