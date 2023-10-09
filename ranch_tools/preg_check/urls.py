from django.urls import path
from .views import PregCheckListView, PregCheckRecordNewAnimalView, PregCheckSummaryStatsView


urlpatterns = [
    path('pregchecks/', PregCheckListView.as_view(), name='pregcheck-list'),
    path('pregchecks/create/', PregCheckRecordNewAnimalView.as_view(), name='pregcheck-create'),
    path('pregchecks/summary-stats/', PregCheckSummaryStatsView.as_view(), name='pregcheck-summary-stats'),
]

