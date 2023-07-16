from django import forms


class AnimalSearchForm(forms.Form):
    animal_id = forms.CharField(label='Animal ID')


class PregCheckForm(forms.Form):
    animal_id = forms.CharField(widget=forms.HiddenInput())
    STATUS_CHOICES = [
        ('P', 'Pregnant'),
        ('O', 'Open'),
    ]
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.RadioSelect)
