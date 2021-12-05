# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc
from dash import html
import plotly as pl
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import project2

app = dash.Dash(__name__)
transport_data = project2.load_transport_data('transport_data_mod.csv')
case_data = project2.load_case_data('covid_cases_mod.csv')

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Dates": [x.date for x in case_data],
    "Cases": [x.new_cases for x in case_data],
    "All Motor Vehicles": [x.cars for x in transport_data]
})

fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(
    go.Line(x=df.get("Dates"), y=df.get("Cases"), name='Cases'),
    secondary_y=False
)

fig.add_trace(
    go.Line(x=df.get("Dates"), y=df.get("All Motor Vehicles"), name='All Motor Vehicle Transport'),
    secondary_y=True
)

fig.update_layout(
    title_text='Cases and All Motor Vehicle Traffic in UK'
)

fig.update_xaxes(title_text='Date')
fig.update_yaxes(title_text='Cases', secondary_y=False)
fig.update_yaxes(title_text='Percent Inc/Dec of Transport Relative to 100%', secondary_y=True)


app.layout = html.Div(children=[
    dcc.Graph(
        id='case-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=False)
