import pytest
from django.urls import reverse

from preg_check.models import Cow, Location, PregCheck


@pytest.mark.django_db
def test_record_pregcheck_new_animal(client):
    local = Location.objects.create(name='Test Location')
    response = client.post(
        reverse('pregcheck-create'),
        {
            'pregcheck_animal_id': 'A006',
            'birth_year': 2021,
            'breeding_season': 2023,
            'comments': 'Test Comment',
            'location': f'{local.id}',
            'preg_status': 'P',
        }
    )
    assert response.status_code == 302
    assert Cow.objects.filter(animal_id='A006').exists()

@pytest.mark.django_db
def test_record_pregcheck_existing_animal(client):
    cow = Cow.objects.create(animal_id='A007', birth_year=2022)
    local = Location.objects.create(name='Test Location')
    response = client.post(
        reverse('pregcheck-create'),
        {
            'pregcheck_animal_id': 'A007',
            'birth_year': 2022,
            'breeding_season': 2023,
            'comments': 'Test Comment',
            'location': f'{local.id}',
            'preg_status': 'P',
        }
    )
    assert response.status_code == 302
    assert Cow.objects.filter(animal_id='A007').count() == 1
    assert PregCheck.objects.count() == 1

