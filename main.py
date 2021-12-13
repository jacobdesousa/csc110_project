"""
CSC110: Project Part 2
Jacob DeSousa, Marco Marchesano, Siddharth Arya
Analysis of COVID-19 case data in relation to transportation trends in the UK.
This file creates the graph to display the data found in the csv files as well as
performs some computations on the data.

Run this app with "Run File in Python Console" or "python main.py" and
visit http://127.0.0.1:8050 in your web browser.
"""

import dash
import python_ta
import web_app
import get_files


app = dash.Dash(__name__)

if __name__ == '__main__':
    python_ta.check_all(config={
        'extra-imports': ['web_app', 'get_files', 'dash', 'python_ta'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
    get_files.download_datasets()

    web_app.create_layout(app)
    app.run_server(debug=False)
