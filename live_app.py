"""
This script creates a Dash app that displays live histograms and scatter plots
based on data from a JSON file.
"""

import json
from datetime import datetime

import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px


def load_data():
    """
    Load data from the JSON file and return a DataFrame with Date and Type columns.
    """
    with open('fake_users.json', 'r', encoding='utf-8') as file:
        user_data = json.load(file)

    created_at_data = [datetime.strptime(user['created_at'], '%Y-%m-%d') for user in user_data]
    updated_at_data = [datetime.strptime(user['updated_at'], '%Y-%m-%d') for user in user_data]

    intertwined_data = []
    for created, updated in zip(created_at_data, updated_at_data):
        intertwined_data.append({'Date': created, 'Type': 'Created At'})
        intertwined_data.append({'Date': updated, 'Type': 'Updated At'})

    return pd.DataFrame(intertwined_data)


app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Live Histogram and Scatter Plot"),
    dcc.Graph(id='live-histogram'),
    dcc.Graph(id='live-scatter-plot'),
    dcc.Interval(
        id='interval-component',
        interval=1 * 1000,  # Update every second
        n_intervals=0
    )
])


@app.callback(Output('live-histogram', 'figure'), Input('interval-component', 'n_intervals'))
def update_histogram(n):  # pylint: disable=unused-argument
    """
    Update the histogram based on the current data in the JSON file.
    """
    data_frame = load_data()
    fig = px.histogram(
        data_frame, x='Date', nbins=50,
        color='Type', title='Created At and Updated At Histogram'
    )
    return fig


@app.callback(Output('live-scatter-plot', 'figure'), Input('interval-component', 'n_intervals'))
def update_scatter_plot(n):  # pylint: disable=unused-argument
    """
    Update the scatter plot based on the current data in the JSON file.
    """
    data_frame = load_data()
    fig = px.scatter(
        data_frame, x='Date',
        color='Type', title='Created At and Updated At Scatter Plot'
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
