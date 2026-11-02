from rest_framework import serializers
from .models import Investigation, TimelineEntry, InvestigationSuggestion


class InvestigationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investigation
        fields = [
            'id', 'lost_report', 'user', 'status',
            'ai_summary', 'created_at', 'updated_at',
        ]

        read_only_fields = [
            'id', 'user', 'status',
            'ai_summary', 'created_at', 'updated_at'
        ]


class TimelineEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = TimelineEntry
        fields = [
            'id',
            'investigation',
            'place',
            'description',
            'visited_at',
            'sequence',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class InvestigationSuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestigationSuggestion
        fields = [
            'id', 'investigation', 'suggestion_type',
            'title', 'description', 'reason',
            'is_completed', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class InvestigationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investigation
        fields = ['status']

class SuggestionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestigationSuggestion
        fields = ['is_completed']