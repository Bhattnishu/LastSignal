from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import ItemReport, RecoveryRequest, ItemMatch, Notification
from .serializers import (
    ItemReportSerializer,
    RecoveryRequestSerializer,
    ItemMatchSerializer,
    RecoveryRequestResponseSerializer,
    NotificationSerializer,
)
from .matching import calculate_match_score


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
                match, created = ItemMatch.objects.get_or_create(
                    lost_report=lost_report,
                    found_report=found_report,
                    defaults={
                        'score': result['score'],
                        'reasons': result['reasons']
                    }
                )

                if not match.is_notified:
                    Notification.objects.get_or_create(
                        user=lost_report.user,
                        match=match,
                        defaults={
                            'title': 'Possible match found!',
                            'message': (
                                f"Someone reported finding an item "
                                f"that may match your lost {lost_report.item_name}."
                            )
                        }
                    )

                    match.is_notified = True
                    match.save(update_fields=['is_notified'])


class MyReportsView(generics.ListAPIView):
    serializer_class = ItemReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ItemReport.objects.filter(
            user=self.request.user
        )


class MyReportDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ItemReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ItemReport.objects.filter(user=self.request.user)


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
        recovery_request = serializer.save(
            requester=self.request.user
        )

        result = calculate_match_score(
            recovery_request.lost_report,
            recovery_request.found_report
        )

        match, created = ItemMatch.objects.get_or_create(
            lost_report=recovery_request.lost_report,
            found_report=recovery_request.found_report,
            defaults={
                'score': result['score'],
                'reasons': result['reasons']
            }
        )

        Notification.objects.get_or_create(
            user=recovery_request.found_report.user,
            match=match,
            defaults={
                'title': 'New Recovery Request!',
                'message': (
                    f'{self.request.user.name} has requested '
                    f'recovery of your found '
                    f'{recovery_request.found_report.item_name}.'
                )
            }
        )

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


class MyNotificationsView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user
        ).select_related(
            'match',
            'match__lost_report',
            'match__found_report'
        )


class NotificationMarkReadView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        notification = get_object_or_404(
            Notification,
            pk=pk,
            user=request.user
        )

        notification.is_read = True
        notification.save(update_fields=['is_read'])

        return Response({
            'message': 'Notification marked as read.',
            'is_read': True
        }, status=status.HTTP_200_OK)
