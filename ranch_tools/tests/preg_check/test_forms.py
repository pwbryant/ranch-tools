import pytest

from preg_check.forms import AnimalSearchForm, PregCheckForm
from preg_check.models import Cow, Location, PregCheck


@pytest.mark.django_db
def test_animal_search_form_valid():
    form = AnimalSearchForm(data={'search_animal_id': 'A001'})
    assert form.is_valid()


@pytest.mark.django_db
def test_animal_search_form_invalid():
    form = AnimalSearchForm(data={'search_animal_id': ''})
    assert not form.is_valid()


@pytest.mark.django_db
def test_pregcheck_form_valid():
    cow = Cow.objects.create(animal_id='A003', birth_year=2019)
    local = Location.objects.create(name='Test Location')

    form = PregCheckForm(data={
        'pregcheck_animal_id': 'A003',
        'birth_year': 2019,
        'breeding_season': 2022,
        'comments': 'Test Comment',
        'location': f'{local.id}',
        'preg_status': 'P',
    })
    assert form.is_valid()


@pytest.mark.django_db
def test_pregcheck_form_invalid():
    form = PregCheckForm(data={})
    assert not form.is_valid()

