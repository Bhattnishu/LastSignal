from rest_framework import serializers
from .models import ItemReport, RecoveryRequest, ItemMatch


class ItemReportSerializer(serializers.ModelSerializer):

    user_name = serializers.CharField(
        source='user.name',
        read_only=True
    )

    class Meta:
        model = ItemReport
        fields = [
            'id',
            'user',
            'user_name',
            'report_type',
            'item_name',
            'category',
            'description',
            'brand',
            'color',
            'image',
            'location',
            'city',
            'occurred_at',
            'status',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'user',
            'status',
            'created_at',
            'updated_at',
        ]


class RecoveryRequestSerializer(serializers.ModelSerializer):

    requester_name = serializers.CharField(
        source='requester.name',
        read_only=True
    )

    class Meta:
        model = RecoveryRequest
        fields = [
            'id',
            'lost_report',
            'found_report',
            'requester',
            'requester_name',
            'message',
            'status',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'requester',
            'requester_name',
            'status',
            'created_at',
            'updated_at',
        ]

    def validate(self, data):

        request = self.context['request']

        lost_report = data['lost_report']
        found_report = data['found_report']

        if lost_report.report_type != ItemReport.ReportType.LOST:
            raise serializers.ValidationError(
                "The selected report must be a LOST report."
            )

        if found_report.report_type != ItemReport.ReportType.FOUND:
            raise serializers.ValidationError(
                "The selected report must be a FOUND report."
            )

        if lost_report.user != request.user:
            raise serializers.ValidationError(
                "You can only request recovery for your own lost item."
            )

        if found_report.status != ItemReport.Status.ACTIVE:
            raise serializers.ValidationError(
                "This found-item report is no longer active."
            )

        if found_report.user == request.user:
            raise serializers.ValidationError(
                "You cannot send a recovery request for your own found report."
            )

        return data

    def validate_status(self, value):
        if value not in [
            RecoveryRequest.RequestStatus.ACCEPTED,
            RecoveryRequest.RequestStatus.REJECTED,
        ]:
            raise serializers.ValidationError("Invalid response status.")
        return value


class RecoveryRequestResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecoveryRequest
        fields = ['status']

    def validate_status(self, value):
        if value not in [
            RecoveryRequest.RequestStatus.ACCEPTED,
            RecoveryRequest.RequestStatus.REJECTED
        ]:
            raise serializers.ValidationError(
                "You can only accept or reject a recovery request."
            )
        return value


class ItemMatchSerializer(serializers.ModelSerializer):
    lost_item_name = serializers.CharField(
        source='lost_report.item_name',
        read_only=True
    )
    found_item_name = serializers.CharField(
        source='found_report.item_name',
        read_only=True
    )

    class Meta:
        model = ItemMatch
        fields = [
            'id',
            'lost_report',
            'found_report',
            'lost_item_name',
            'found_item_name',
            'score',
            'reasons',
            'created_at',
        ]
        read_only_fields = fields
