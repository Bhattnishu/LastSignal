from django.contrib import admin
from .models import (
    Investigation,
    TimelineEntry,
    InvestigationSuggestion
)


@admin.register(Investigation)
class InvestigationAdmin(admin.ModelAdmin):
    list_display = ('id', 'lost_report', 'user', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('lost_report__item_name', 'user__email')


@admin.register(TimelineEntry)
class TimelineEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'investigation', 'place', 'visited_at', 'sequence')
    search_fields = ('place', 'description')


@admin.register(InvestigationSuggestion)
class InvestigationSuggestionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'investigation', 'title',
        'suggestion_type', 'is_completed'
    )
    list_filter = ('suggestion_type', 'is_completed')
    search_fields = ('title', 'description')
