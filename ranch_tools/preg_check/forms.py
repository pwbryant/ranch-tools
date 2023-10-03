from django import forms

from .models import PregCheck

from pdb import set_trace as bp


class AnimalSearchForm(forms.Form):
    search_animal_id = forms.CharField(label='Animal ID')


class PregCheckForm(forms.ModelForm):
    pregcheck_animal_id = forms.CharField(label='Animal ID', required=False)
    birth_year = forms.CharField(label='Birth Year', required=False)
    is_pregnant = forms.ChoiceField(
        label='Status',
        choices=((True, 'Pregnant'), (False, 'Open')),
        widget=forms.RadioSelect(),
        required=True,
    )

    # def clean_is_pregnant(self):
    #     is_pregnant = self.cleaned_data.get('is_pregnant')
    #     if is_pregnant is None:
    #         raise forms.ValidationError("Please select either 'Open' or 'Pregnant'.")
    #     return is_pregnant

    class Meta:
        model = PregCheck
        fields = ['is_pregnant', 'breeding_season', 'comments']
        widgets = {
            'is_pregnant': forms.RadioSelect(choices=((True, 'Pregnant'), (False, 'Open'))),
            'breeding_season': forms.TextInput(attrs={'pattern': '\d{4}', 'title': 'Please enter a four-digit year'}),
            'comments': forms.Textarea,
        }

