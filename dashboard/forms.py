from django import forms
from dashboard import models


class CsvUploadForm(forms.Form):
    nomdataset = forms.CharField(label='NOM DU DATASET',widget=forms.TextInput(attrs={'class':"form-controll"}))
    category = forms.ChoiceField(label='CATEGORY',
                                 choices=list(models.Categories.objects.values_list('id', 'NomCategory')), widget=forms.Select(attrs={'class':"form-controll"}))
    pays = forms.ChoiceField(label='PAYS', choices=list(models.Pays.objects.values_list('id', 'NomPays')),widget=forms.Select(attrs={'class':"form-controll"}))
    annee = forms.ChoiceField(label='ANNEE', choices=list(models.Annee.objects.values_list('id', 'annee')),widget=forms.Select(attrs={'class':"form-controll"}))
    sep = forms.BooleanField(label='SEPATATEUR is ;', widget=forms.CheckboxInput(attrs={'class':"form-controll"}),required=False)
    csv = forms.FileField(label='Select a CSV file', help_text='ONLY CSV files allowed')
