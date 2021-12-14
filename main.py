"""
CSC110: Project Part 2
Jacob DeSousa, Marco Marchesano, Siddharth Arya
Analysis of COVID-19 case data in relation to transportation trends in the UK.
This file sets up the program, and has the callback method update_graph to
represent any live changes in the graph.

Run this app with "Run File in Python Console" or "python main.py" and
visit http://127.0.0.1:8050 in your web browser.
"""

import webbrowser
import dash
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import python_ta

import web_app
import get_files

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
    fig.update_yaxes(title_text='Confirmed Covid-19 Cases', secondary_y=False)
    fig.update_yaxes(title_text='Percent of Transportation used', secondary_y=True)

    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    return fig


if __name__ == '__main__':
    # python_ta.check_all(config={
    #     'extra-imports': ['web_app', 'get_files', 'dash', 'python_ta', 'plotly',
    #                       'dash.dependencies', 'plotly.graph_objects', 'plotly.subplots',
    #                       'webbrowser'],
    #     'allowed-io': [],
    #     'max-line-length': 100,
    #     'disable': ['R1705', 'C0200']
    # })
    get_files.download_datasets()

    web_app.create_layout(app)
    webbrowser.open('http://127.0.0.1:8050')
    app.run_server(debug=False)
