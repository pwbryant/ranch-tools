from django.urls import path
from .views import PregCheckListView, PregCheckRecordNewAnimalView

urlpatterns = [
    path('pregchecks/', PregCheckListView.as_view(), name='pregcheck-list'),
    path('pregchecks/create/', PregCheckRecordNewAnimalView.as_view(), name='pregcheck-create'),
]

