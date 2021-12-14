"""
CSC110: Project Part 2
Jacob DeSousa, Marco Marchesano, Siddharth Arya

The web_app module handles creating the output for the project.
It handles creating the graph figure and the HTML layout for the interactive pieces.

Copyright (c) 2021 || Jacob DeSousa, Marco Marchesano, Siddharth Arya
"""

import doctest
import dash
from dash import dcc, html
import pandas as pd
import python_ta.contracts

import data_manip
from data_manip import average_case_data, average_transport_data


def make_df(grouping: int) -> pd.DataFrame:
    """
    Returns a pandas dataframe with averaged data from the datasets based on grouping.

    :param grouping: The number of entries in the datasets to average together.
    :return: A dataframe which is based on datasets and modified to fit grouping.
    """
    averaged_case_data = \
        average_case_data(data_manip.load_case_data('covid_cases_mod.csv'), grouping)
    averaged_transportation_data = \
        average_transport_data(data_manip.load_transport_data('transport_data_mod.csv'), grouping)
    return pd.DataFrame({
        "Dates": [x.date for x in averaged_case_data],
        "Cases": [x.new_cases for x in averaged_case_data],
        "Cars": [x.cars for x in averaged_transportation_data],
        "Light Commercial Vehicles": [x.light_commercial_vehicles
                                      for x in averaged_transportation_data],
        "Heavy Goods Vehicles": [x.heavy_goods_vehicles for x in averaged_transportation_data],
        "All Motor Vehicles": [x.all_motor_vehicles for x in averaged_transportation_data],
        "National Rail": [x.national_rail for x in averaged_transportation_data],
        "London Tube": [x.london_tube for x in averaged_transportation_data],
        "London Buses": [x.london_buses for x in averaged_transportation_data],
        "National Buses": [x.national_buses for x in averaged_transportation_data],
        "Cycling": [x.cycling for x in averaged_transportation_data]
    })


def create_layout(app_to_modify: dash.Dash) -> None:
    """
    Modifies the layout attribute of the Dash app app_to_modify.

    :param app_to_modify: The app object from the outer class.
    :return: No return. Method mutates app_to_modify.
    """
    app_to_modify.layout = html.Div([
        html.H1(
            children='CSC110: Project Part 2',
            style={'textAlign': 'center', 'color': '#131313'}
        ),
        html.H3(
            children='Jacob DeSousa, Marco Marchesano, Siddharth Arya',
            style={'textAlign': 'center', 'color': '#131313'}
        ),
        html.Div(children=[
            html.Tbody(children='The graphic below shows confirmed cases in the UK by date, '
                                'and different selected modes of travel. The modes of travel are '
                                'represented as a percentage of an equivalent day or week prior to'
                                ' the COVID-19 pandemic.',
                       style={'textAlign': 'left', 'color': '#131313'}
                       ),
            html.Tbody(children='The average factor slider will adjust how often a data point'
                                ' should be represented. The datasets include daily metrics,'
                                ' but for a smoother graph a higher average factor can be'
                                ' selected. Depending on that value, days will be averaged'
                                ' together to represent data points less often.',
                       style={'textAlign': 'left', 'color': '#131313'}
                       ),
            html.Tbody(children='Data points that were missing from the transportation dataset'
                                ' will be represented as -1 on the graph.',
                       style={'textAlign': 'left', 'color': '#131313'}
                       )
        ]),
        dcc.Graph(id='graphic', ),
        html.Div(children=[
            html.Label('Select Modes of Transportation:'),
            dcc.Checklist(
                id='modes',
                options=[
                    {'label': 'Cars', 'value': 'Cars'},
                    {'label': 'Light Commercial Vehicles', 'value': 'Light Commercial Vehicles'},
                    {'label': 'Heavy Goods Vehicles', 'value': 'Heavy Goods Vehicles'},
                    {'label': 'All Motor Vehicles', 'value': 'All Motor Vehicles'},
                    {'label': 'National Rail', 'value': 'National Rail'},
                    {'label': 'London Tube', 'value': 'London Tube'},
                    {'label': 'London Buses', 'value': 'London Buses'},
                    {'label': 'National Buses', 'value': 'National Buses'},
                    {'label': 'Cycling', 'value': 'Cycling'},
                ],
                value=[],
                style={'display': 'flex', 'flex-direction': 'column'}
            ),

            html.Br(),
            html.Div(children=[
                html.Label('Average Factor:'),
                dcc.Slider(
                    id='average_factor',
                    min=1,
                    max=30,
                    marks={i: i if i % 5 == 0 else '' for i in range(1, 31)},
                    value=5
                )
            ]),
        ], style={'width': '35%', 'horizontalAlign': 'left'}),

        html.Div(children=[
            html.H3(children='Data by Individual Date:',
                    style={'textAlign': 'left', 'color': '#131313'}
                    ),
            html.Tbody(children='Please input a date in yyyy/mm/dd format to retrieve case and '
                                'transport data for that particular day.',
                       style={'textAlign': 'left', 'color': '#131313'}
                       ),
            dcc.Input(id='date-input', value='yyyy/mm/dd', type='text')
        ]),
        html.Div(id='data-output')
    ])


if __name__ == '__main__':
    doctest.testmod()
    python_ta.contracts.check_all_contracts()
    python_ta.check_all(config={
        'extra-imports': ['pandas', 'python_ta', 'dash', 'data_manip', 'doctest'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
