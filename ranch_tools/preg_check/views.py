from datetime import datetime
import json
from urllib.parse import urlencode

from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, CreateView, FormView
from django.views.generic.edit import UpdateView

from .forms import (
    AnimalSearchForm,
    CowForm,
    EditPregCheckForm,
    PregCheckForm
)
from .models import Cow, CurrentBreedingSeason, PregCheck

from pdb import set_trace as bp


class PregCheckListView(ListView):
    model = PregCheck
    template_name = 'pregcheck_list.html'
    context_object_name = 'pregchecks'

    def get_queryset(self):
        animal_id = self.request.GET.get('search_animal_id', None)
        birth_year = self.request.GET.get('search_birth_year', None)
        if animal_id and animal_id.strip().lower() == 'all':
            current_breeding_season = CurrentBreedingSeason.load().breeding_season
            queryset = PregCheck.objects.filter(breeding_season=current_breeding_season).order_by('-check_date')
        elif animal_id:
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
        pregcheck_form = PregCheckForm()
        animals = Cow.objects.filter(animal_id=animal_id)
        if birth_year:
            animals = animals.filter(birth_year=birth_year)
            pregcheck_form.fields['birth_year'].initial = birth_year
        animal_exists = None
        if animal_id:
            animal_exists = Cow.objects.filter(animal_id=animal_id).exists()
            pregcheck_form.fields['pregcheck_animal_id'].initial = animal_id

        animal_count = animals.count()
        cow = None
        if animal_count == 1:
            cow = animals[0]
            distinct_birth_years = [cow.birth_year]
            birth_year = cow.birth_year
        else:
            distinct_birth_years = animals.values_list('birth_year', flat=True).distinct()

        search_form = AnimalSearchForm(
            initial={'search_animal_id': animal_id, 'search_birth_year': birth_year},
            birth_year_choices=[(y, str(y),) for y in distinct_birth_years]
        )
        pregcheck_form.fields['breeding_season'].initial = datetime.now().year
        current_breeding_season = CurrentBreedingSeason.load().breeding_season
        if animal_count == 1:
            preg_checks_this_season = PregCheck.objects.filter(
                cow=cow, breeding_season=current_breeding_season
            ).count()
            pregcheck_form.fields['recheck'].initial = preg_checks_this_season > 0

        context['current_breeding_season'] = current_breeding_season
        context['all_preg_checks'] = False if animal_id is None else animal_id.strip().lower() == 'all'
        context['latest_breeding_season'] = PregCheck.objects.latest('id').breeding_season
        context['search_form'] = search_form
        context['pregcheck_form'] = pregcheck_form
        context['animal_exists'] = animal_exists
        context['multiple_matches'] = animal_count > 1
        context['distinct_birth_years'] = distinct_birth_years
        context['cow'] = cow
        return context


class UpdateCurrentBreedingSeasonView(View):

    def post(self, request, *args, **kwargs):
        try:
            # Assuming you're sending data as JSON
            data = json.loads(request.body)
            breeding_season = int(data.get('breeding_season'))
            current_season = CurrentBreedingSeason.load()
            current_season.breeding_season = breeding_season
            current_season.save()
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


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
        stats_breeding_season = request.GET.get('stats_breeding_season')

        if not stats_breeding_season:
            return HttpResponseBadRequest("stats_breeding_season parameter is required.")

        all_checks = PregCheck.objects.filter(breeding_season=stats_breeding_season)
        total_pregnant_count = all_checks.filter(is_pregnant=True).count()
        all_opens_count = all_checks.filter(is_pregnant=False).count()

        rechecks = all_checks.filter(recheck=True)
        preg_rechecks_count = rechecks.filter(is_pregnant=True).count()
        open_rechecks_count = rechecks.filter(is_pregnant=False).count()

        first_pass_pregs_count = total_pregnant_count - preg_rechecks_count
        first_pass_open_count = all_opens_count - open_rechecks_count

        total_open_count = first_pass_open_count - preg_rechecks_count
        total_count = total_open_count + total_pregnant_count
        pregnancy_rate = (total_pregnant_count / total_count) * 100 if total_count > 0 else 0

        summary_stats = {
            'first_check_pregnant': first_pass_pregs_count,
            'recheck_pregnant': preg_rechecks_count,
            'total_pregnant': total_pregnant_count,
            'first_check_open': first_pass_open_count,
            'less_recheck_pregnant': preg_rechecks_count,
            'total_open': total_open_count,
            'total_count': total_count,
            'pregnancy_rate': pregnancy_rate
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


class CowUpdateView(UpdateView):
    model = Cow
    fields = ['birth_year']
    template_name = 'path_to_template.html'  # Replace with the path to your template for updating the cow
    
    def form_valid(self, form):
        # Save the updated cow instance
        self.object = form.save()

        # Construct the URL for redirection
        redirect_url = reverse('pregcheck-list')
        query_parameters = {
            'search_animal_id': self.object.animal_id,
            'search_birth_year': form.cleaned_data['birth_year']
        }
        full_redirect_url = redirect_url + '?' + urlencode(query_parameters)
        
        return redirect(full_redirect_url)
    
    def get_success_url(self):
        # This method might not be called due to our custom redirection in form_valid method, but just in case:
        return reverse('pregcheck-list')


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

