"""
CSC110: Project Part 2
Jacob DeSousa, Marco Marchesano, Siddharth Arya

The web_app module handles creating the output for the project.
It handles creating the graph figure and the HTML layout for the interactive pieces.
"""

import dash
from dash import dcc, html
import pandas as pd
import python_ta

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
                value=[]
            )
        ], style={'width': '100%', 'display': 'inline-block'}),
        dcc.Graph(id='graphic', ),
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
        ], style={'width': '35%'})
    ])


if __name__ == '__main__':
    python_ta.check_all(config={
        'extra-imports': ['pandas', 'python_ta', 'dash', 'data_manip'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
