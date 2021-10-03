from django import forms


class LocationForm(forms.Form):
    name = forms.CharField()
    lat = forms.FloatField()
    lng = forms.FloatField()