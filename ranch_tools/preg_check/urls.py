from django.urls import path
from .views import PregCheckListView, PregCheckCreateView

urlpatterns = [
    path('pregchecks/', PregCheckListView.as_view(), name='pregcheck-list'),
    path('pregchecks/create/', PregCheckCreateView.as_view(), name='pregcheck-create'),
]

