
from rest_framework import serializers
from .models import ItemReport, RecoveryRequest, ItemMatch, Notification


class ItemReportSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = ItemReport
        fields = [
            'id', 'user', 'user_name', 'report_type',
            'item_name', 'category', 'description',
            'brand', 'color', 'image', 'location',
            'city', 'occurred_at', 'status',
            'created_at', 'updated_at',
        ]
        read_only_fields = [
            'id', 'user', 'status', 'created_at', 'updated_at',
        ]


class RecoveryRequestSerializer(serializers.ModelSerializer):
    requester_name = serializers.CharField(
        source='requester.name', read_only=True
    )
    found_by_name = serializers.CharField(
        source='found_report.user.name', read_only=True
    )
    lost_item_name = serializers.CharField(
        source='lost_report.item_name', read_only=True
    )
    found_item_name = serializers.CharField(
        source='found_report.item_name', read_only=True
    )

    class Meta:
        model = RecoveryRequest
        fields = [
            'id',
            'lost_report',
            'found_report',
            'requester',
            'requester_name',
            'found_by_name',
            'lost_item_name',
            'found_item_name',
            'message',
            'contact_method',
            'contact_value',
            'response_message',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'requester',
            'requester_name',
            'found_by_name',
            'lost_item_name',
            'found_item_name',
            'response_message',
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
                "The selected report must be a lost item."
            )

        if found_report.report_type != ItemReport.ReportType.FOUND:
            raise serializers.ValidationError(
                "The selected report must be a found item."
            )

        if lost_report.user != request.user:
            raise serializers.ValidationError(
                "You can only request recovery for your own lost item."
            )

        if found_report.status != ItemReport.Status.ACTIVE:
            raise serializers.ValidationError(
                "This found item is no longer available."
            )

        if found_report.user == request.user:
            raise serializers.ValidationError(
                "You cannot request your own found item."
            )

        if not data.get('message', '').strip():
            raise serializers.ValidationError(
                "Please enter a message."
            )

        if not data.get('contact_method'):
            raise serializers.ValidationError(
                "Please select Phone or Email."
            )

        if not data.get('contact_value', '').strip():
            raise serializers.ValidationError(
                "Please provide your contact details."
            )

        return data


# Kept temporarily because the existing views.py imports this serializer.
class RecoveryRequestResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecoveryRequest
        fields = [
            'status',
            'response_message',
            'contact_method',
            'contact_value',
        ]

    def validate(self, data):
        status = data.get('status', self.instance.status)

        if status not in [
            RecoveryRequest.RequestStatus.ACCEPTED,
            RecoveryRequest.RequestStatus.REJECTED,
        ]:
            raise serializers.ValidationError("Invalid response status.")

        return data


class ItemMatchSerializer(serializers.ModelSerializer):
    lost_item_name = serializers.CharField(
        source='lost_report.item_name', read_only=True
    )
    found_item_name = serializers.CharField(
        source='found_report.item_name', read_only=True
    )
    found_item_image = serializers.ImageField(
        source='found_report.image', read_only=True
    )

    class Meta:
        model = ItemMatch
        fields = [
            'id', 'lost_report', 'found_report',
            'lost_item_name', 'found_item_name',
            'found_item_image',
            'score', 'reasons', 'created_at',
        ]
        read_only_fields = fields

class NotificationSerializer(serializers.ModelSerializer):
    match_id = serializers.IntegerField(
        source='match.id', read_only=True
    )
    lost_report_id = serializers.IntegerField(
        source='match.lost_report.id', read_only=True
    )
    found_report_id = serializers.IntegerField(
        source='match.found_report.id', read_only=True
    )

    class Meta:
        model = Notification
        fields = [
            'id', 'title', 'message', 'is_read',
            'match_id', 'lost_report_id',
            'found_report_id', 'created_at',
        ]
        read_only_fields = fields
