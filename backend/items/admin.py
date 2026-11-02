
from django.contrib import admin
from .models import ItemReport, RecoveryRequest


@admin.register(ItemReport)
class ItemReportAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'item_name', 'report_type',
        'category', 'city', 'status', 'created_at'
    )
    list_filter = ('report_type', 'category', 'status', 'city')
    search_fields = ('item_name', 'description', 'city', 'brand')


@admin.register(RecoveryRequest)
class RecoveryRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'lost_report', 'found_report',
        'requester', 'status', 'created_at'
    )
    list_filter = ('status',)
    search_fields = ('message',)
