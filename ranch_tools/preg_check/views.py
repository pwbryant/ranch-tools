from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from .forms import AnimalSearchForm, PregCheckForm
from .models import Cow, PregCheck

from pdb import set_trace as bp



class PregCheckCreateView(FormView):
    form_class = PregCheckForm
    template_name = 'pregcheck_create.html'
    success_url = reverse_lazy('pregcheck-list')

    def form_valid(self, form):
        # Handle form submission logic here
        animal_id = form.cleaned_data['animal_id']
        status = form.cleaned_data['status']
        # Perform the necessary operations, e.g., create a new PregCheck instance

        return super().form_valid(form)


class PregCheckListView(ListView):
    model = PregCheck
    template_name = 'pregcheck_list.html'
    context_object_name = 'pregchecks'

    def get_queryset(self):
        animal_id = self.request.GET.get('animal_id', None)
        if animal_id:
            queryset = PregCheck.objects.filter(cow__animal_id=animal_id).order_by('-check_date')[:3]
        else:
            queryset = PregCheck.objects.none()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        animal_id = self.request.GET.get('animal_id', None)
        search_form = AnimalSearchForm(initial={'animal_id': animal_id})
        pregcheck_form = PregCheckForm()
        if animal_id and self.object_list.exists():
            pregcheck_form.fields['animal_id'].initial = animal_id
            pregcheck_form.fields['status'].widget.attrs['disabled'] = False
        else:
            pregcheck_form.fields['animal_id'].widget.attrs['disabled'] = True
        context['search_form'] = search_form
        context['pregcheck_form'] = pregcheck_form
        return context

