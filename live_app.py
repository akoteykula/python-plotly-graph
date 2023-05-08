import json
import pandas as pd
from datetime import datetime
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px


# Load data from the JSON file
def load_data():
    with open('fake_users.json', 'r') as f:
        user_data = json.load(f)

    created_at_data = [datetime.strptime(user['created_at'], '%Y-%m-%d') for user in user_data]
    updated_at_data = [datetime.strptime(user['updated_at'], '%Y-%m-%d') for user in user_data]

    intertwined_data = []
    for created, updated in zip(created_at_data, updated_at_data):
        intertwined_data.append({'Date': created, 'Type': 'Created At'})
        intertwined_data.append({'Date': updated, 'Type': 'Updated At'})

    return pd.DataFrame(intertwined_data)


# Create a Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Live Histogram"),
    dcc.Graph(id='live-histogram'),
    dcc.Interval(
        id='interval-component',
        interval=1 * 1000,  # Update every second
        n_intervals=0
    )
])


# App callback
@app.callback(Output('live-histogram', 'figure'), Input('interval-component', 'n_intervals'))
def update_histogram(n):
    df = load_data()
    fig = px.histogram(df, x='Date', nbins=50, color='Type', title='Created At and Updated At Histogram')
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)