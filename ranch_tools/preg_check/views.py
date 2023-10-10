from datetime import datetime

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, CreateView, FormView

from .models import Cow, PregCheck
from .forms import AnimalSearchForm, CowForm, PregCheckForm

from pdb import set_trace as bp


class PregCheckListView(ListView):
    model = PregCheck
    template_name = 'pregcheck_list.html'
    context_object_name = 'pregchecks'

    def get_queryset(self):
        animal_id = self.request.GET.get('search_animal_id', None)
        birth_year = self.request.GET.get('search_birth_year', None)
        if animal_id:
            queryset = PregCheck.objects.filter(cow__animal_id=animal_id)
            if birth_year:
                queryset = queryset.filter(cow__birth_year=birth_year)
            queryset = queryset.order_by('-check_date', '-id')[:3]
        else:
            queryset = PregCheck.objects.none()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        animal_id = self.request.GET.get('search_animal_id', None)
        birth_year = self.request.GET.get('search_birth_year', None)
        search_form = AnimalSearchForm(initial={'search_animal_id': animal_id, 'search_birth_year': birth_year})
        animals = Cow.objects.filter(animal_id=animal_id)
        if birth_year:
            animals = animals.filter(birth_year=birth_year)
        animal_count = animals.count()
        distinct_birth_years = Cow.objects.filter(animal_id=animal_id).values_list('birth_year', flat=True).distinct()
        pregcheck_form = PregCheckForm()
        animal_exists = Cow.objects.filter(animal_id=animal_id).exists()

        if animal_id:
            pregcheck_form.fields['pregcheck_animal_id'].initial = animal_id

        pregcheck_form.fields['breeding_season'].initial = datetime.now().year

        context['search_form'] = search_form
        context['pregcheck_form'] = pregcheck_form
        context['animal_exists'] = animal_exists
        context['multiple_matches'] = animal_count > 1
        context['distinct_birth_years'] = distinct_birth_years
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

        if animal_id:
            birth_year = None if not birth_year else birth_year
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


class PregCheckSummaryStatsView(View):
    def get(self, request, *args, **kwargs):
        # Calculate your summary stats here
        total_pregnant = PregCheck.objects.filter(is_pregnant=True).count()
        total_open = PregCheck.objects.filter(is_pregnant=False).count()
        total_count = PregCheck.objects.count()

        # Calculate pregnancy rate (percentage)
        pregnancy_rate = (total_pregnant / total_count) * 100 if total_count > 0 else 0

        # Prepare the data as a dictionary
        summary_stats = {
            'total_pregnant': total_pregnant,
            'total_open': total_open,
            'total_count': total_count,
            'pregnancy_rate': pregnancy_rate,
        }

        # Return the data as JSON response
        return JsonResponse(summary_stats)


class CowCreateView(CreateView):
    model = Cow
    form_class = CowForm  # Replace with your actual form class
# template_name = 'cow_create.html'  # Replace with your desired template

# Override the success URL
    def get_success_url(self):
        return reverse('pregcheck-list')  # Redirect to the desired page after creating a Cow

    # def form_valid(self, form):
# # Process the form data and create a new Cow instance
# # Here, you can also handle the optional birth_year field
    #     animal_id = form.cleaned_data['animal_id']
    #     birth_year = form.cleaned_data.get('birth_year')

# # Create a new Cow instance
    #     bp()
    #     Cow.objects.create(animal_id=animal_id, birth_year=birth_year)

    #     return super().form_valid(form)

    # def post(self, request, *args, **kwargs):
    #     """
    #     Handle POST requests: instantiate a form instance with the passed
    #     POST variables and then check if it's valid.
    #     """
    #     form = self.get_form()
    #     bp()
    #     if form.is_valid():
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)


