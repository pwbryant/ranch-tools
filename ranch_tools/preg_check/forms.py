from django import forms

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
    class Meta:
        model = PregCheck
        fields = ['is_pregnant', 'comments', 'recheck']

