from django.shortcuts import render
from django.http import HttpResponse
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import os
from .forms import CountriesForm


""" class base_pandas():

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

        return pivot """


def get_path(path):
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, path)
    return file_path

# Create your views here.
class base_pandas:

    def __init__(self):
        self.composite = None


    def add_composite(self, composite):
        self.composite = composite


    def select_columns(self, columns_list, dataframe):
        result = dataframe[columns_list]
        return result


    def select_countries(self, countries_list, dataframe):
        df = dataframe
        result = df[df['country'].isin(countries_list)]
        return result


    def groupby_and_get_mean(self, groupby_list, dataframe):
        result = dataframe.groupby(groupby_list).mean().reset_index()
        return result


    """ def pivot_reshape(self, pivot_list, dataframe):
        result = dataframe.pivot(index=pivot_list[0], columns=pivot_list[1], values=pivot_list[2])
        return result """


    def define_dataframe(self, columns_list, countries_list, groupby_list, dataframe, path):
        columns = self.select_columns(columns_list, dataframe)
        countries = self.select_countries(countries_list, columns)
        groupby = self.groupby_and_get_mean(groupby_list, countries)
        # pivot = self.pivot_reshape(pivot_list, groupby)


        self.composite.init(groupby, path)

        # return result



class by_year():

    def init(self, dataframe, path):

        df = dataframe.pivot(index='year' , columns='country' , values='suicides/100k pop')

        df.plot().get_figure().savefig(path)



class by_age():

    def init(self, dataframe, path):
        df = dataframe.pivot(index='country' , columns='age' , values='suicides/100k pop')

        columns_order = ['5-14 years', '15-24 years', '25-34 years', '35-54 years', '55-74 years', '75+ years']
        df = df.reindex(columns_order, axis=1 )
        df.plot.barh().get_figure().savefig(path)



class by_sex():

    def init(self, dataframe, path): 
        df = dataframe.pivot(index='country' , columns='sex' , values='suicides/100k pop')
        df.plot.barh().get_figure().savefig(path) 


#views

def index(request):

    context = {}
    context['has_image'] = False

    countries_form = CountriesForm()

    if request.method == 'POST' and 'countries' in request.POST:

        countries_form = CountriesForm(request.POST)

        if countries_form.is_valid():

            csv_path = get_path('csv/master.csv')
            df = pd.read_csv(csv_path)

            countries_list = request.POST.getlist('countries')

            

            by = request.POST.get('by')

            columns_list = ['country', by, 'suicides/100k pop']
            groupby_list = ['country', by]



            plot_path = get_path('static/plots/plot.png')

            if by == 'year':
                # pivot_list = [by, 'country', 'suicides/100k pop']

                # result = define_dataframe(columns_list, countries_list, groupby_list, pivot_list, df)
                # result.plot().get_figure().savefig(plot_path)
                year_instance = base_pandas()
                year_instance.add_composite(by_year())
                year_instance.define_dataframe(columns_list, countries_list, groupby_list, df, plot_path)

                context['title_plot'] = 'taxa de suicídio por ano'

            elif by == 'age':
                # pivot_list = ['country', by, 'suicides/100k pop']

                # define_df = define_dataframe(columns_list, countries_list, groupby_list, pivot_list, df)
                # columns_order = ['5-14 years', '15-24 years', '25-34 years', '35-54 years', '55-74 years', '75+ years']
                # result = define_df.reindex(columns_order, axis=1 )
                # result.plot.bar().get_figure().savefig(plot_path)

                year_instance = base_pandas()
                year_instance.add_composite(by_age())
                year_instance.define_dataframe(columns_list, countries_list, groupby_list, df, plot_path)

                context['title_plot'] = 'Média de  suicídios por idade'

            elif by == 'sex':
                # pivot_list = ['country', by, 'suicides/100k pop']

                # result = define_dataframe(columns_list, countries_list, groupby_list, pivot_list, df)
                # result.plot.bar().get_figure().savefig(plot_path)

                year_instance = base_pandas()
                year_instance.add_composite(by_sex())
                year_instance.define_dataframe(columns_list, countries_list, groupby_list, df, plot_path)

                context['title_plot'] = 'Média de  suicídios por sexo'
    
    context['form'] = countries_form

    return render(request, 'index.html', context)
