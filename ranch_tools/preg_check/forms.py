from django import forms

from .models import PregCheck



class AnimalSearchForm(forms.Form):
    search_animal_id = forms.CharField(label='Animal ID')


class PregCheckForm(forms.ModelForm):
    pregcheck_animal_id = forms.CharField(label='Animal ID')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['preg_status'].widget.choices = [('P', 'Pregnant'), ('O', 'Open')]
        self.fields['pregcheck_animal_id'].widget.attrs['readonly'] = True


    class Meta:
        model = PregCheck
        fields = ['preg_status', 'location', 'breeding_season', 'comments']
        widgets = {
            'preg_status': forms.RadioSelect,
            'location': forms.Select,
            'breeding_season': forms.TextInput(attrs={'pattern': '\d{4}', 'title': 'Please enter a four-digit year'}),
            'comments': forms.Textarea,
        }

