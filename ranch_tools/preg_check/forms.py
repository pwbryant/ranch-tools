from django import forms
from django.core.exceptions import ValidationError

from .models import Cow, PregCheck

from pdb import set_trace as bp


class AnimalSearchForm(forms.Form):

    def __init__(self, *args, **kwargs):
        birth_year_choices = kwargs.pop('birth_year_choices', [])
        super().__init__(*args, **kwargs)
        self.fields['search_birth_year'] = forms.ChoiceField(
            choices=birth_year_choices,
            widget=forms.RadioSelect,
            required=False
        )
    search_animal_id = forms.CharField(label='Animal ID')


class PregCheckForm(forms.ModelForm):
    pregcheck_animal_id = forms.CharField(label='Animal ID', required=False)
    birth_year = forms.CharField(required=False, widget=forms.HiddenInput())
    is_pregnant = forms.ChoiceField(
        label='Status',
        choices=((True, 'Pregnant'), (False, 'Open')),
        widget=forms.RadioSelect(),
        required=True,
    )
    recheck = forms.BooleanField(label='Recheck', required=False, widget=forms.CheckboxInput())

    class Meta:
        model = PregCheck
        fields = ['is_pregnant', 'breeding_season', 'comments', 'recheck']
        widgets = {
            'is_pregnant': forms.RadioSelect(choices=((True, 'Pregnant'), (False, 'Open'))),
            'breeding_season': forms.TextInput(attrs={'pattern': '\d{4}', 'title': 'Please enter a four-digit year'}),
            'comments': forms.Textarea,
        }


class CowForm(forms.ModelForm):
    class Meta:
        model = Cow
        fields = ['animal_id', 'birth_year']

    animal_id = forms.CharField(
        label='Animal ID',
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    birth_year = forms.CharField(
        label='Birth Year (optional)',
        max_length=4,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'YYYY'})
    )


class EditPregCheckForm(forms.ModelForm):
    animal_id = forms.CharField(max_length=10, required=False)
    birth_year = forms.CharField(max_length=4, required=False)

    class Meta:
        model = PregCheck
        fields = ['animal_id', 'birth_year', 'breeding_season', 'is_pregnant', 'comments', 'recheck']

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if self.instance.cow:
                self.fields['animal_id'].initial = self.instance.cow.animal_id
                self.fields['birth_year'].initial = self.instance.cow.birth_year

    def clean(self):
        cleaned_data = super().clean()
        animal_id = cleaned_data.get('animal_id')
        birth_year = cleaned_data.get('birth_year')
        if animal_id and birth_year:
            try:
                cow = Cow.objects.get(animal_id=animal_id, birth_year=birth_year)
            except Cow.DoesNotExist:
                raise ValidationError(f"No cow found with animal_id {animal_id} and birth_year {birth_year}")
        elif animal_id:
            try:
                cow = Cow.objects.get(animal_id=animal_id)
            except Cow.DoesNotExist:
                raise ValidationError(f"No cow found with animal_id {animal_id}")

        return cleaned_data

    def save(self, commit=True):
        preg_check = super().save(commit=False)
        animal_id = self.cleaned_data.get('animal_id')
        birth_year = self.cleaned_data.get('birth_year')
        
        if animal_id:
            try:
                cow = Cow.objects.get(animal_id=animal_id, birth_year=birth_year)
                preg_check.cow = cow
            except Cow.DoesNotExist:
                # This shouldn't happen due to clean_animal_id, but just in case
                raise ValidationError(f"No cow found with animal_id {animal_id}")

        if commit:
            preg_check.save()
        return preg_check
