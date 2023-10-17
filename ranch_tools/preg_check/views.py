from datetime import datetime
from urllib.parse import urlencode

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, CreateView, FormView

from .forms import AnimalSearchForm, CowForm, EditPregCheckForm, PregCheckForm
from .models import Cow, PregCheck

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
            queryset = queryset.order_by('-check_date', '-id')
        else:
            queryset = PregCheck.objects.none()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        animal_id = self.request.GET.get('search_animal_id', None)
        birth_year = self.request.GET.get('search_birth_year', None)
        search_form = AnimalSearchForm(initial={'search_animal_id': animal_id, 'search_birth_year': birth_year})
        pregcheck_form = PregCheckForm()
        animals = Cow.objects.filter(animal_id=animal_id)
        if birth_year:
            animals = animals.filter(birth_year=birth_year)
            pregcheck_form.fields['birth_year'].initial = birth_year
        distinct_birth_years = Cow.objects.filter(animal_id=animal_id).values_list('birth_year', flat=True).distinct()
        animal_exists = None
        if animal_id:
            animal_exists = Cow.objects.filter(animal_id=animal_id).exists()
            pregcheck_form.fields['pregcheck_animal_id'].initial = animal_id

        animal_count = animals.count()

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
        birth_year = None if not birth_year else birth_year
        if animal_id and birth_year:
            cow, created = Cow.objects.get_or_create(animal_id=animal_id, birth_year=birth_year)
            form.instance.cow = cow
        elif animal_id:
            cow, created = Cow.objects.get_or_create(animal_id=animal_id)
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
        total_pregnant = PregCheck.objects.filter(is_pregnant=True).count()
        total_open = PregCheck.objects.filter(is_pregnant=False).count()
        total_count = PregCheck.objects.count()

        pregnancy_rate = (total_pregnant / total_count) * 100 if total_count > 0 else 0

        summary_stats = {
            'total_pregnant': total_pregnant,
            'total_open': total_open,
            'total_count': total_count,
            'pregnancy_rate': pregnancy_rate,
        }

        return JsonResponse(summary_stats)


class CowCreateView(CreateView):
    model = Cow
    form_class = CowForm

    def get_success_url(self):
        cow = self.object
        query_parameters = {
            'search_animal_id': cow.animal_id,
            'search_birth_year': cow.birth_year
        }
        url = reverse('pregcheck-list') + '?' + urlencode(query_parameters)
        return url



class PregCheckEditView(View):
    def post(self, request, pregcheck_id):
        try:
            pregcheck = PregCheck.objects.get(pk=pregcheck_id)
        except PregCheck.DoesNotExist:
            return JsonResponse({'error': 'PregCheck not found'}, status=404)

        form = EditPregCheckForm(request.POST, instance=pregcheck)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': 'PregCheck updated successfully'})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'errors': errors}, status=400)


class PregCheckDetailView(View):

    def get(self, request, pregcheck_id):
        # Retrieve the PregCheck object or return a 404 response if not found
        pregcheck = get_object_or_404(PregCheck, pk=pregcheck_id)
        
        pregcheck_details = {
            'id': pregcheck.id,
            'is_pregnant': pregcheck.is_pregnant,
            'comments': pregcheck.comments,
            'recheck': pregcheck.recheck,
        }

        return JsonResponse(pregcheck_details)

