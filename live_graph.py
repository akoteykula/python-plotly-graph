import json
import random
from datetime import datetime
from faker import Faker
import dash
from dash import html
from dash import dcc
import pandas as pd
from dash.dependencies import Input, Output

# Initialize the Faker library
fake = Faker()


# Generate a new fake user
def generate_fake_user():
    created_at = fake.date_between(start_date='-5y', end_date='today')
    updated_at = fake.date_between(start_date=created_at, end_date='today')

    return {
        "name": fake.name(),
        "email": fake.email(),
        "date_of_birth": fake.date_of_birth().strftime('%Y-%m-%d'),
        "created_at": created_at.strftime('%Y-%m-%d'),
        "updated_at": updated_at.strftime('%Y-%m-%d')
    }


# Initialize the Dash app
app = dash.Dash(__name__)

# Set up the app layout
app.layout = html.Div([
    html.H1('Live Updating User Table'),
    dcc.Interval(id='interval-component', interval=1000, n_intervals=0),  # Update every second
    html.Div(id='live-table')
])


# Update the table with new data every second
@app.callback(Output('live-table', 'children'),
              Input('interval-component', 'n_intervals'))
def update_table(n):
    # Generate new fake data
    user_data = [generate_fake_user() for _ in range(10)]

    # Create a DataFrame with the data
    df = pd.DataFrame(user_data)

    # Convert the DataFrame to an HTML table
    table = html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in df.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(df.iloc[i][col]) for col in df.columns
            ]) for i in range(len(df))
        ])
    ])

    return table


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)