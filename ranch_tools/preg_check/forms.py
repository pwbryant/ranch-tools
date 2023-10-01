from django import forms

from .models import PregCheck


class AnimalSearchForm(forms.Form):
    search_animal_id = forms.CharField(label='Animal ID')


class PregCheckForm(forms.ModelForm):
    pregcheck_animal_id = forms.CharField(label='Animal ID', required=False)
    birth_year = forms.CharField(label='Birth Year', required=False)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
        # self.fields['pregcheck_animal_id'].widget.attrs['readonly'] = True

    class Meta:
        model = PregCheck
        fields = ['is_pregnant', 'breeding_season', 'comments']
        widgets = {
            'is_pregnant': forms.RadioSelect(choices=((True, 'Pregnant'), (False, 'Open'))),
            'breeding_season': forms.TextInput(attrs={'pattern': '\d{4}', 'title': 'Please enter a four-digit year'}),
            'comments': forms.Textarea,
        }

