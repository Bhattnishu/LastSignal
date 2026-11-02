from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
\
from .models import ItemReport
from .serializers import ItemReportSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .matching import calculate_match_score
from .models import ItemReport, RecoveryRequest
from .models import ItemReport, RecoveryRequest, ItemMatch
from .serializers import ItemReportSerializer, RecoveryRequestSerializer
from .serializers import (
    ItemReportSerializer,
    RecoveryRequestSerializer,
    ItemMatchSerializer,
    RecoveryRequestResponseSerializer,
)

class ItemReportCreateView(generics.CreateAPIView):
    queryset = ItemReport.objects.all()
    serializer_class = ItemReportSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        report = serializer.save(user=self.request.user)

        if report.status != ItemReport.Status.ACTIVE:
            return

        if report.report_type == ItemReport.ReportType.LOST:
            opposite_reports = ItemReport.objects.filter(
                report_type=ItemReport.ReportType.FOUND,
                status=ItemReport.Status.ACTIVE
            ).exclude(user=self.request.user)

        else:
            opposite_reports = ItemReport.objects.filter(
                report_type=ItemReport.ReportType.LOST,
                status=ItemReport.Status.ACTIVE
            ).exclude(user=self.request.user)

        for opposite_report in opposite_reports:
            if report.report_type == ItemReport.ReportType.LOST:
                lost_report = report
                found_report = opposite_report
            else:
                lost_report = opposite_report
                found_report = report

            result = calculate_match_score(lost_report, found_report)

            if result['score'] >= 20:
                ItemMatch.objects.get_or_create(
                    lost_report=lost_report,
                    found_report=found_report,
                    defaults={
                        'score': result['score'],
                        'reasons': result['reasons']
                    }
                )

class MyReportsView(generics.ListAPIView):
    serializer_class = ItemReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ItemReport.objects.filter(
            user=self.request.user
        )


class MyReportDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ItemReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ItemReport.objects.filter(
            user=self.request.user
        )


class FoundReportsView(generics.ListAPIView):
    serializer_class = ItemReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ItemReport.objects.filter(
            report_type=ItemReport.ReportType.FOUND,
            status=ItemReport.Status.ACTIVE
        )


class ItemMatchesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        # Find the lost report belonging to the logged-in user
        lost_report = get_object_or_404(
            ItemReport,
            pk=pk,
            user=request.user,
            report_type=ItemReport.ReportType.LOST
        )

        # Get all active found reports
        found_reports = ItemReport.objects.filter(
            report_type=ItemReport.ReportType.FOUND,
            status=ItemReport.Status.ACTIVE,
            category=lost_report.category
        ).exclude(user=request.user)

        matches = []

        # Compare the lost report with every found report
        for found_report in found_reports:

            result = calculate_match_score(
                lost_report,
                found_report
            )

            if result['score'] >= 20:
                matches.append({
                    'report': ItemReportSerializer(found_report).data,
                    'match_score': result['score'],
                    'match_reasons': result['reasons']
                })

        # Highest matching score first
        matches.sort(
            key=lambda item: item['match_score'],
            reverse=True
        )

        return Response({
            'lost_report_id': lost_report.id,
            'total_matches': len(matches),
            'matches': matches
        }, status=status.HTTP_200_OK)


class RecoveryRequestCreateView(generics.CreateAPIView):
    queryset = RecoveryRequest.objects.all()
    serializer_class = RecoveryRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)


class MySentRecoveryRequestsView(generics.ListAPIView):
    serializer_class = RecoveryRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RecoveryRequest.objects.filter(
            requester=self.request.user
        ).select_related('lost_report', 'found_report', 'requester')


class MyReceivedRecoveryRequestsView(generics.ListAPIView):
    serializer_class = RecoveryRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RecoveryRequest.objects.filter(
            found_report__user=self.request.user
        ).select_related('lost_report', 'found_report', 'requester')


class RecoveryRequestUpdateView(generics.UpdateAPIView):
    serializer_class = RecoveryRequestResponseSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch']

    def get_queryset(self):
        return RecoveryRequest.objects.filter(
            found_report__user=self.request.user,
            status=RecoveryRequest.RequestStatus.PENDING
        )

    def perform_update(self, serializer):
        serializer.save()

class MyMatchesView(generics.ListAPIView):
    serializer_class = ItemMatchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ItemMatch.objects.filter(
            Q(lost_report__user=self.request.user) |
            Q(found_report__user=self.request.user)
        ).select_related('lost_report', 'found_report')
