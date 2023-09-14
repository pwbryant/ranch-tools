from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.views.generic import ListView, CreateView, FormView

from .models import Cow, PregCheck
from .forms import AnimalSearchForm, PregCheckForm


class PregCheckListView(ListView):
    model = PregCheck
    template_name = 'pregcheck_list.html'
    context_object_name = 'pregchecks'

    def get_queryset(self):
        animal_id = self.request.GET.get('search_animal_id', None)
        if animal_id:
            queryset = PregCheck.objects.filter(cow__animal_id=animal_id).order_by('-check_date', '-id')[:3]
        else:
            queryset = PregCheck.objects.none()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        animal_id = self.request.GET.get('search_animal_id', None)
        search_form = AnimalSearchForm(initial={'search_animal_id': animal_id})
        pregcheck_form = PregCheckForm()
        animal_exists = Cow.objects.filter(animal_id=animal_id).exists()

        if animal_id and self.object_list.exists():
            pregcheck_form.fields['pregcheck_animal_id'].initial = animal_id
            pregcheck_form.fields['preg_status'].widget.attrs['disabled'] = False
        else:
            pregcheck_form.fields['preg_status'].widget.attrs['disabled'] = True

        context['search_form'] = search_form
        context['pregcheck_form'] = pregcheck_form
        context['animal_exists'] = animal_exists
        return context


class PregCheckRecordNewAnimalView(CreateView):
    model = PregCheck
    form_class = PregCheckForm
    # template_name = 'pregcheck_list.html'

    def get(self, request, *args, **kwargs):
       # This view only handles POST requests, so for GET requests,
       # simply redirect to PregCheckListView.
        return HttpResponseRedirect(reverse('pregcheck-list'))

    def get_initial(self):
        initial = super().get_initial()
        animal_id = self.kwargs.get('animal_id')
        if animal_id:
            initial['pregcheck_animal_id'] = animal_id
        return initial

    def form_valid(self, form):
        animal_id = form.cleaned_data['pregcheck_animal_id']
        birth_year = form.cleaned_data['birth_year']

        cow, created = Cow.objects.get_or_create(animal_id=animal_id, defaults={'birth_year': birth_year})
        form.instance.cow = cow

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('pregcheck-list')

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
