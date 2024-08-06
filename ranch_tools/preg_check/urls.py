from django.urls import path
from .views import (
    CowCreateView,
    CowUpdateView,
    PregCheckDetailView,
    PregCheckEditView,
    PregCheckListView,
    PregCheckRecordNewAnimalView,
    PregCheckSummaryStatsView,
    PreviousPregCheckListView,
    UpdateCurrentBreedingSeasonView,
)


urlpatterns = [
    path('cows/create/', CowCreateView.as_view(), name='cow-create'),
    path('cows/<int:pk>/update/', CowUpdateView.as_view(), name='cow-update'),
    path('pregchecks/', PregCheckListView.as_view(), name='pregcheck-list'),
    path('pregchecks/current-breeding-season/', UpdateCurrentBreedingSeasonView.as_view(), name='pregcheck-breeding-season'),
    path('pregchecks/create/', PregCheckRecordNewAnimalView.as_view(), name='pregcheck-create'),
    path('pregchecks/summary-stats/', PregCheckSummaryStatsView.as_view(), name='pregcheck-summary-stats'),
    path('pregchecks/previous-pregchecks/', PreviousPregCheckListView.as_view(), name='previous-pregchecks'),
    path('pregchecks/<int:pregcheck_id>/edit/', PregCheckEditView.as_view(), name='pregcheck-edit'),
    path('pregchecks/<int:pregcheck_id>/', PregCheckDetailView.as_view(), name='pregcheck-detail'),
]

