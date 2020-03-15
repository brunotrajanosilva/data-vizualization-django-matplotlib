from django.shortcuts import render
from django.http import HttpResponse
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import os
from .forms import CountriesForm


# Create your views here.

def get_path(path):
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, path)
    return file_path


def select_columns(columns_list, dataframe):
    result = dataframe[columns_list]
    return result


def select_countries(countries_list, dataframe):
    df = dataframe
    result = df[df['country'].isin(countries_list)]
    return result


def groupby_and_get_mean(groupby_list, dataframe):
    result = dataframe.groupby(groupby_list).mean().reset_index()
    return result


def pivot_reshape(pivot_list, dataframe):
    result = dataframe.pivot(index=pivot_list[0], columns=pivot_list[1], values=pivot_list[2])
    return result


def define_dataframe(columns_list, countries_list, groupby_list, pivot_list, dataframe):
    columns = select_columns(columns_list, dataframe)
    countries = select_countries(countries_list, columns)
    groupby = groupby_and_get_mean(groupby_list, countries)
    pivot = pivot_reshape(pivot_list, groupby)

    return pivot



#views

def index(request):

    context = {}
    context['has_image'] = False

    if request.method == 'POST' and 'countries' in request.POST:

        csv_path = get_path('csv/master.csv')
        df = pd.read_csv(csv_path)

        countries_list = request.POST.getlist('countries')
        by = request.POST.get('by')

        columns_list = ['country', by, 'suicides/100k pop']
        groupby_list = ['country', by]



        plot_path = get_path('static/plots/plot.png')

        if by == 'year':
            pivot_list = [by, 'country', 'suicides/100k pop']

            result = define_dataframe(columns_list, countries_list, groupby_list, pivot_list, df)
            result.plot().get_figure().savefig(plot_path)

            context['title_plot'] = 'taxa de suicídio por ano'

        elif by == 'age':
            pivot_list = ['country', by, 'suicides/100k pop']

            define_df = define_dataframe(columns_list, countries_list, groupby_list, pivot_list, df)
            columns_order = ['5-14 years', '15-24 years', '25-34 years', '35-54 years', '55-74 years', '75+ years']
            result = define_df.reindex(columns_order, axis=1 )
            result.plot.bar().get_figure().savefig(plot_path)

            context['title_plot'] = 'Média de  suicídios por idade'

        elif by == 'sex':
            pivot_list = ['country', by, 'suicides/100k pop']

            result = define_dataframe(columns_list, countries_list, groupby_list, pivot_list, df)
            result.plot.bar().get_figure().savefig(plot_path)

            context['title_plot'] = 'Média de  suicídios por sexo'
    
    context['form'] = CountriesForm()

    return render(request, 'index.html', context)
