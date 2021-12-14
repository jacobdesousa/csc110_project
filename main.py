"""
CSC110: Project Part 2
Jacob DeSousa, Marco Marchesano, Siddharth Arya
Analysis of COVID-19 case data in relation to transportation trends in the UK.
This file sets up the program, and has the callback method update_graph to
represent any live changes in the graph.

Run this app with "Run File in Python Console" or "python main.py" and
visit http://127.0.0.1:8050 in your web browser.
"""

import datetime
import webbrowser

import dash
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots

import data_manip
import get_files
import web_app

app = dash.Dash(__name__)


@app.callback(
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
    df = web_app.make_df(average_factor)

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
    fig.update_yaxes(title_text='Confirmed COVID-19 Cases', secondary_y=False)
    fig.update_yaxes(title_text='Percent of Transportation Used', secondary_y=True)

    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    return fig


@app.callback(
    Output('data-output', 'children'),
    Input('date-input', 'value')
)
def update_data_box(date_input) -> str:
    case_data = data_manip.load_case_data('covid_cases_mod.csv')
    transport_data = data_manip.load_transport_data('transport_data_mod.csv')

    date = datetime.date(int(date_input[0:4]), int(date_input[5:7]), int(date_input[8:10]))
    date_case_data = None
    date_transport_data = None
    for x in case_data:
        if x.date == date:
            date_case_data = x
    for x in transport_data:
        if x.date == date:
            date_transport_data = x
    if date_case_data is None or date_transport_data is None:
        return ''
    else:
        return 'New Cases: ' + str(date_case_data.new_cases) + \
               ' || Cumulative Cases: ' + str(date_case_data.cum_cases) + \
               ' || Cars: ' + str(date_transport_data.cars) + '%' + \
               ' || Light Commercial Vehicles: ' + \
               str(date_transport_data.light_commercial_vehicles) + '%' + \
               ' || Heavy Goods Vehicles: ' + \
               str(date_transport_data.heavy_goods_vehicles) + '%' + \
               ' || All Motor Vehicles: ' + str(date_transport_data.all_motor_vehicles) + '%' + \
               ' || National Rail: ' + str(date_transport_data.national_rail) + '%' + \
               ' || London Tube: ' + str(date_transport_data.london_tube) + '%' + \
               ' || London Buses: ' + str(date_transport_data.london_buses) + '%' + \
               ' || National Buses: ' + str(date_transport_data.national_buses) + '%' + \
               ' || Cycling: ' + str(date_transport_data.cycling) + '%'


if __name__ == '__main__':
    get_files.download_datasets()

    web_app.create_layout(app)
    webbrowser.open('http://127.0.0.1:8050')
    app.run_server(debug=False)
