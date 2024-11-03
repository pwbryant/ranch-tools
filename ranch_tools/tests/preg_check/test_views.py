import pytest
from django.urls import reverse

from preg_check.models import Cow, PregCheck


@pytest.mark.django_db
def test_record_pregcheck_new_animal(client):
    response = client.post(
        reverse('pregcheck-create'),
        {
            'pregcheck_ear_tag_id': 'A006',
            'birth_year': 2021,
            'breeding_season': 2023,
            'comments': 'Test Comment',
            'preg_status': 'P',
        }
    )
    assert response.status_code == 302
    assert Cow.objects.filter(ear_tag_id='A006').exists()


@pytest.mark.django_db
def test_record_pregcheck_existing_animal(client):
    cow = Cow.objects.create(ear_tag_id='A007', birth_year=2022)
    response = client.post(
        reverse('pregcheck-create'),
        {
            'pregcheck_ear_tag_id': 'A007',
            'birth_year': 2022,
            'breeding_season': 2023,
            'comments': 'Test Comment',
            'preg_status': 'P',
        }
    )
    assert response.status_code == 302
    assert Cow.objects.filter(ear_tag_id='A007').count() == 1
    assert PregCheck.objects.count() == 1


@pytest.mark.django_db
def test_record_pregcheck_no_ear_tag_id(client):
    response = client.post(
        reverse('pregcheck-create'),
        {
            'birth_year': 2022,
            'breeding_season': 2023,
            'comments': 'Test Comment',
            'preg_status': 'P',
        }
    )
    assert response.status_code == 302
    assert Cow.objects.filter(ear_tag_id='A007').count() == 0
    assert PregCheck.objects.count() == 1

