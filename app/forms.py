from django import forms
from django.db.models import fields 
from django.core.exceptions import ValidationError


class UserInputForm(forms.Form):
    start = forms.DateField(label="Date start " ,widget=forms.DateInput(format='%m/%d/%Y',attrs={'class': 'datepicker'}) , input_formats=('%Y-%m-%d', ) )
    end = forms.DateField(label="Date end",widget=forms.DateInput(format='%m/%d/%Y',attrs={'class': 'datepicker'}) ,input_formats=('%Y-%m-%d', ))
    latitude = forms.FloatField(label="latitude",widget=forms.HiddenInput(),required=False)
    longititude = forms.FloatField(label="Longititude" ,widget=forms.HiddenInput(),required=False)

    def clean_end(self):
            data = self.cleaned_data['end']
            if data < self.cleaned_data['start']:
                raise ValidationError("End date should be superior to start date!")

            # Always return a value to use as the new cleaned data, even if
            # this method didn't change it.
            return data

            