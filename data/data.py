import requests
import json
from collections import defaultdict, OrderedDict
import matplotlib.pyplot as plt
'exec(%matplotlib inline)'
import pandas as pd
import numpy as np
import plotly.colors
import plotly.graph_objs as go


country_default = OrderedDict([('Canada', 'CN'), ('United States', 'US'),
    ('Brazil', 'Br'), ('China', 'CN'), ('Japan', 'JP'), ('Russia', 'RU'),
    ('Germany', 'DE'), ('Inda', 'IN'), ('France', 'FR'), ('Italy', 'IT'),
    ('United Kingdom', 'GB'), ('Korea, Rep', 'KR'), ('Spain', 'ES'),
    ('Australia', 'AU'), ('Mexico', 'MX')])



def return_figures(countries = country_default):

    if not bool(countries):
        countries=country_default
    country_filter = list(countries.values())
    country_filter = [x.lower() for x in country_filter]
    country_filter = ';'.join(country_filter)

    indicators = ['NY.GNP.PCAP.CD', 'NY.GDP.MKTP.CD', 'SP.POP.TOTL',
        'FP.CPI.TOTL.ZG', 'EG.ELC.ACCS.ZS']

    data_frames = []
    urls = []

    for indicator in indicators:
        url = 'http://api.worldbank.org/v2/countries/'+country_filter+\
        '/indicators/'+indicator+'?date=1990:2019&per_page=2000&format=json'

        urls.append(url)

        try:
            r = requests.get(url)
            data = r.json()[1]
        except:
            print('could not load data', indicator)

        for i, value in enumerate(data):
            value['indicator'] = value['indicator']['value']
            value['country'] = value['country']['value']

        data_frames.append(data)

    graph_one = []
    df_one = pd.DataFrame(data_frames[0])

    df_one = df_one[['indicator','country','date','value']].dropna()
    df_one_yearly_avg = df_one.groupby(['date'], as_index = False).agg({'value':'mean'}
    ).sort_values(by = 'date', ascending = True)
    df_one_yearly_avg.round(2)

    date_list = df_one_yearly_avg.date.unique().tolist()


    x_val = df_one_yearly_avg['date']
    y_val = df_one_yearly_avg.value
    graph_one.append(
    go.Bar(
        x = x_val,
        y = y_val,
        name = date_list
        )
    )

    layout_one = dict(title = "Average Gross National Income(GNI) <br>\
In the Top 20 Economies of the World",
                xaxis = dict(title = 'Year',
                  autotick=False, tick0=1990, dtick=28),
                yaxis = dict(title = 'Average GNI($)'),
                )

    graph_two = []
    df_one_country = df_one

    print(df_one_country)
    countrylist = df_one.country.unique().tolist()
    for country in countrylist:
      x_val = df_one_country[df_one_country['country'] == country].date.tolist()
      y_val = df_one_country[df_one_country['country'] == country].value.tolist()
      date = df_one_country[df_one_country['country'] == country].date.tolist()
      country_label = df_one_country[df_one_country['country'] == country].country.tolist()

      text = []
      for country, date in zip(country_label, date):
          text.append(str(country) + ' ' + str(date))
      graph_two.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          text = text,
          name = country,
          textposition = 'top'
          )
      )

      layout_two = dict(title = 'GNI Per Capita for Each Country',
                  xaxis = dict(title = 'Year',
                    autotick=False, tick0=1990, dtick=28),
                  yaxis = dict(title = 'Gross National Income($)'),
                  )

    graph_three = []
    df_three = pd.DataFrame(data_frames[2])
    df_three = df_three[df_three.date!='2019']


    countrylist = df_three.country.unique().tolist()
    for country in countrylist:
      x_val = df_three[df_three['country'] == country].date.tolist()
      y_val = df_three[df_three['country'] == country].value.tolist()
      date = df_three[df_three['country'] == country].date.tolist()
      country_label = df_three[df_three['country'] == country].country.tolist()

      text = []
      for country, date in zip(country_label, date):
          text.append(str(country) + ' ' + str(date))
      graph_three.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          text = text,
          name = country,
          textposition = 'top'
          )
      )

      layout_three = dict(title = 'Total Population Per Country',
                  xaxis = dict(title = 'Year',
                    autotick=False, tick0=1990, dtick=28),
                  yaxis = dict(title = 'Populatioin Total'),
                  )


    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))











    return figures
