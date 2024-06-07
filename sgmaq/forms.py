from django import forms

class WashForm(forms.Form):
    license_plate_photo = forms.ImageField(label='Foto de la Matrícula')
