from django.urls import path
from .views import SuggestionUpdateView,InvestigationCreateView,InvestigationUpdateView, InvestigationSuggestionCreateView,TimelineEntryCreateView, MySuggestionsView,MyTimelineView

urlpatterns = [
    path('', InvestigationCreateView.as_view(), name='investigation-create'),
    path(
        'timeline/',
        TimelineEntryCreateView.as_view(),
        name='timeline-create'
    ),
    path(
        'my-timeline/',
        MyTimelineView.as_view(),
        name='my-timeline'
    ),
    path(
        'suggestions/',
        InvestigationSuggestionCreateView.as_view(),
        name='suggestion-create'
    ),
    path(
        'my-suggestions/',
        MySuggestionsView.as_view(),
        name='my-suggestions'
    ),
    path(
        '<int:pk>/',
        InvestigationUpdateView.as_view(),
        name='investigation-update'
    ),
    path(
        'suggestions/<int:pk>/',
        SuggestionUpdateView.as_view(),
        name='suggestion-update'
    ),
]