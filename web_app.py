"""
CSC110: Project Part 2
Jacob DeSousa, Marco Marchesano, Siddharth Arya

The web_app module handles creating the output for the project.
It handles creating the graph figure and the HTML layout for the interactive pieces.
"""

import main
import data_manip
from data_manip import average_case_data, average_transport_data
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import python_ta


def make_df(grouping: int) -> pd.DataFrame:
    """
    Returns a pandas dataframe with averaged data from the datasets based on grouping.

    :param grouping: The number of entries in the datasets to average together.
    :return: A dataframe which is based on datasets and modified to fit grouping.
    """
    averaged_case_data = average_case_data(data_manip.load_case_data('covid_cases_mod.csv'), grouping)
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

        # html.H3("Enter any date below to see the data for the given date (please follow a yyyy/mm/dd "
        #         "format)"),
        # html.Div([
        #     "Input Date: ",
        #     dcc.Input(id='my-input', value='yyyy/mm/dd', type='text')
        # ]),
        # html.Br(),
        # html.Div(id='my-output')
    ])


@main.app.callback(
    Output('graphic', 'figure'),
    Input('average_factor', 'value'),
    Input('modes', 'value'),

)
def update_graph(average_factor: int, modes: list[str]) -> go.Figure:
    """
    This method returns the figure to be displayed as the graph.
    It is called whenever an option is changed on the main page.

    :param average_factor: The input from the slider on the main page.
    :param modes: A list of the checkboxes selected on the main page.
    :return: Returns a figure including the data type modes and averaged with average_factor.
    """
    df = make_df(average_factor)

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Line(x=df.get("Dates"), y=df.get("Cases"), name='Cases'),
        secondary_y=False
    )
    for x in modes:
        fig.add_trace(
            go.Line(x=df.get("Dates"), y=df.get(x), name=x),
            secondary_y=True
        )
    colours = {
        'background': '#D2F0F3',
        'text': '#131313'
    }
    fig.update_layout(
        plot_bgcolor=colours['background'],
        font_color=colours['text'],
    )

    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='Confirmed Covid-19 Cases', secondary_y=False)
    fig.update_yaxes(title_text='Percent of Transportation used', secondary_y=True)

    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    return fig


# @app.callback(
#     dash.dependencies.Output(component_id='my-output', component_property='children'),
#     dash.dependencies.Input(component_id='my-input', component_property='value')
# )
# def update_output_div(input_value):
#     date = datetime.date(int(input_value[0:4]), int(input_value[5:7]), int(input_value[8:10]))
#     sp_cases = ''
#     sp_cars = ''
#     sp_national_rail = ''
#     sp_national_buses = ''
#     for a1 in case_data:
#         if a1.date == date:
#             sp_cases = str(a1.new_cases)
#
#     for a1 in transport_data:
#         if a1.date == date:
#             sp_cars = str(a1.cars) + '%'
#             sp_national_rail = str(a1.national_rail) + '%'
#             sp_national_buses = str(a1.national_buses) + '%'
#
#     return ('|| New Cases: ' + sp_cases +
#             ', || Cars: ' + sp_cars +
#             ', || National Rail: ' + sp_national_rail +
#             ', || National Buses: ' + sp_national_buses +
#             ' || '
#             )


if __name__ == '__main__':
    python_ta.check_all(config={
        'extra-imports': ['pandas', 'python_ta', 'plotly', 'dash', 'data_manip', 'main'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
