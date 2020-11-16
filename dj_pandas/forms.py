from django import forms
import numpy as np
import pandas as pd
import os





def get_countries_list():
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'csv/master.csv')
    
    df = pd.read_csv(file_path)
    countries = df['country'].unique()

    countries_list = tuple((x,x) for x in countries)

    return countries_list

by_choices = (
    ('year', 'Ano'),
    ('age', 'Idade'),
    ('sex', 'Sexo'),
)

class CountriesForm(forms.Form):
    countries = forms.MultipleChoiceField(choices = get_countries_list, label="Países",
    widget= forms.SelectMultiple(attrs={'class':'selectpicker'}) )
    by = forms.ChoiceField(choices = by_choices, label="Organizar por",
    widget= forms.Select(attrs={'class':'selectpicker'}))


    def clean_countries(self):
        countries = self.cleaned_data['countries']

        if len(countries) > 3:
            raise forms.ValidationError('ocorreu um erro: Selecione até 3 países')

        return countries
