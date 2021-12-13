# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import math
import dash
from dash import dcc
from dash import html
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd
import project2
import datetime

app = dash.Dash(__name__)
transport_data = project2.load_transport_data('transport_data_mod.csv')
case_data = project2.load_case_data('covid_cases_mod.csv')


def average_case_data(data: list[project2.CaseData], grouping: int) -> list[project2.CaseData]:
    """
    Returns a list of averaged data.

    :param data: CaseData objects in a list
    :param grouping: How many entries to average
    :return: List of CaseData averaged

    Preconditions
        - 1 < grouping < 100
    """
    averaged_data = []

    count = len(data)
    while count > 0:
        count -= grouping
        grouped = data[0:min(grouping, len(data))]
        data = data[grouping:len(data)]
        date, new_cases, cum_cases = None, 0, 0
        for i in range(0, min(grouping, len(data))):
            new_cases += grouped[i].new_cases
            cum_cases += grouped[i].cum_cases
            if i == math.ceil(min(grouping, len(data))/2):
                date = grouped[i].date
        averaged_data.append(project2.CaseData(date, round(new_cases / min(grouping, len(grouped))),
                                               round(cum_cases / min(grouping, len(grouped)))))

    return averaged_data


def average_transport_data(data: list[project2.TransportationData], grouping: int)\
        -> list[project2.TransportationData]:
    """
    Calculates the average percentage of each individual form of transportation, the data is
    returned in a list where each element is a given form of transportations percentage of
    average use

    Preconditions
        - 1 < grouping < 100
    """
    averaged_data = []

    count = len(data)
    while count > 0:
        count -= grouping
        grouped = data[0:min(grouping, len(data))]
        data = data[grouping:len(data)]
        date = None
        cars = 0
        lcv = 0
        hgv = 0
        mv = 0
        nr = 0
        lt = 0
        lb = 0
        nb = 0
        cyc = 0
        for i in range(0, min(grouping, len(grouped))):
            cars += grouped[i].cars
            lcv += grouped[i].light_commercial_vehicles
            hgv += grouped[i].heavy_goods_vehicles
            mv += grouped[i].all_motor_vehicles
            nr += grouped[i].national_rail
            lt += grouped[i].london_tube
            lb += grouped[i].london_buses
            nb += grouped[i].national_buses
            cyc += grouped[i].cycling
            if i == math.ceil(min(grouping, len(grouped)) / 2):
                date = grouped[i].date
        averaged_data.append(project2.TransportationData(date,
                                                         round(cars / min(grouping, len(grouped))),
                                                         round(lcv / min(grouping, len(grouped))),
                                                         round(hgv / min(grouping, len(grouped))),
                                                         round(mv / min(grouping, len(grouped))),
                                                         round(nr / min(grouping, len(grouped))),
                                                         round(lt / min(grouping, len(grouped))),
                                                         round(lb / min(grouping, len(grouped))),
                                                         round(nb / min(grouping, len(grouped))),
                                                         round(cyc / min(grouping, len(grouped)))))

    return averaged_data


# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
user_input = int(input('Please enter your value: '))
df = pd.DataFrame({
    "Dates": [x.date for x in average_case_data(case_data, user_input)],
    "Cases": [x.new_cases for x in average_case_data(case_data, user_input)],
    # "All Motor Vehicles": [x.all_motor_vehicles for x in transport_data],
    "Cars": [x.cars for x in average_transport_data(transport_data, user_input)],
    # "Tube": [x.london_tube for x in transport_data]
    "National Rail": [x.national_rail for x in average_transport_data(transport_data, user_input)],
    "National Buses": [x.national_buses for x in average_transport_data(transport_data, user_input)],
    "Cycling": [x.cycling for x in average_transport_data(transport_data, user_input)]
})

fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(
    go.Line(x=df.get("Dates"), y=df.get("Cases"), name='Cases'),
    secondary_y=False
)

fig.add_trace(
    go.Line(x=df.get("Dates"), y=df.get("Cars"), name='Cars'),
    secondary_y=True
)

fig.add_trace(
    go.Line(x=df.get("Dates"), y=df.get("National Rail"), name='National Rail'),
    secondary_y=True
)
fig.add_trace(
    go.Line(x=df.get("Dates"), y=df.get("National Buses"), name='National Buses'),
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

# fig.layout = dict(template='plotly_dark')

# fig.add_trace(
#    go.Line(x=df.get("Dates"), y=df.get("Cycling"), name='Cycling'),
#    secondary_y=True
# )
#
# fig.add_trace(
#     go.Line(x=df.get("Dates"), y=df.get("Cars"), name='Cars'),
#     secondary_y=True
# )
#
# fig.add_trace(
#     go.Line(x=df.get("Dates"), y=df.get("Tube"), name='Tube'),
#     secondary_y=True
# )

fig.update_layout(
    title_text='Cases and All Motor Vehicle Traffic in UK'
)

fig.update_xaxes(title_text='Date')
fig.update_yaxes(title_text='Cases', secondary_y=False)
fig.update_yaxes(title_text='Percent of Transportation used', secondary_y=True)

fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)

app.layout = html.Div(children=[
    html.Header('Select the mode of transportations you would like to see on the graph'),
    html.Div(children=[
        html.Label('Modes of Transportation'),
        dcc.Checklist(
            id='modes',
            options=[
                {'label': 'Cars', 'value': 'CARS'},
                {'label': 'Light Commercial Vehicles', 'value': 'LCV'},
                {'label': 'Heavy Goods Vehicles', 'value': 'HGV'},
                {'label': 'All Motor Vehicles', 'value': 'AMV'},
                {'label': 'National Rail', 'value': 'NR'},
                {'label': 'London Tube', 'value': 'LT'},
                {'label': 'London Buses', 'value': 'LB'},
                {'label': 'National Buses', 'value': 'NB'},
                {'label': 'Cycling', 'value': 'CYC'},
            ],
            value=[]
        )
    ], style={'width': '100%', 'display': 'inline-block'}),

    html.Div(children=[
        dcc.Graph(
            id='case-graph',
            figure=fig
        )
    ]),
    html.H3("Enter any date below to see the data for the given date (please follow a yyyy/mm/dd "
            "format)"),
    html.Div([
        "Input Date: ",
        dcc.Input(id='my-input', value='yyyy/mm/dd', type='text')
    ]),
    html.Br(),
    html.Div(id='my-output')
])


@app.callback(
    Output(component_id='graphic', component_property='figure'),
    Input(component_id='scale', component_property='value'),
    Input('lines', 'value')
)
def update_graph(scale):
    dff = pd.DataFrame({})


@app.callback(
    dash.dependencies.Output(component_id='my-output', component_property='children'),
    dash.dependencies.Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    date = datetime.date(int(input_value[0:4]), int(input_value[5:7]), int(input_value[8:10]))
    sp_cases = ''
    sp_cars = ''
    sp_national_rail = ''
    sp_national_buses = ''
    for a1 in case_data:
        if a1.date == date:
            sp_cases = str(a1.new_cases)

    for a1 in transport_data:
        if a1.date == date:
            sp_cars = str(a1.cars) + '%'
            sp_national_rail = str(a1.national_rail) + '%'
            sp_national_buses = str(a1.national_buses) + '%'

    return ('|| New Cases: ' + sp_cases +
            ', || Cars: ' + sp_cars +
            ', || National Rail: ' + sp_national_rail +
            ', || National Buses: ' + sp_national_buses +
            ' || '
            )


if __name__ == '__main__':
    app.run_server(debug=False)
