
from django.urls import path
from .views import (
    ItemReportCreateView,
    MyReportsView,
    MyReportDetailView,
    FoundReportsView,
    ItemMatchesView,
    MySentRecoveryRequestsView,
    MyReceivedRecoveryRequestsView,
    RecoveryRequestCreateView,
    RecoveryRequestUpdateView,
    MyMatchesView,
)
 

urlpatterns = [
    path('reports/', ItemReportCreateView.as_view(), name='create-report'),
    path('my-reports/', MyReportsView.as_view(), name='my-reports'),
    path(
        'my-reports/<int:pk>/',
        MyReportDetailView.as_view(),
        name='my-report-detail'
    ),
    path('found/', FoundReportsView.as_view(), name='found-reports'),
    path(
        'my-reports/<int:pk>/matches/',
        ItemMatchesView.as_view(),
        name='item-matches'
    ),
    path(
        'recovery-requests/',
        RecoveryRequestCreateView.as_view(),
        name='recovery-request-create'
    ),
    path(
        'recovery-requests/sent/',
        MySentRecoveryRequestsView.as_view(),
        name='recovery-requests-sent'
    ),
    path(
        'recovery-requests/received/',
        MyReceivedRecoveryRequestsView.as_view(),
        name='recovery-requests-received'
    ),
    path(
        'recovery-requests/<int:pk>/respond/',
        RecoveryRequestUpdateView.as_view(),
        name='recovery-request-respond'
    ),
    path('my-matches/', MyMatchesView.as_view(), name='my-matches'),
]
