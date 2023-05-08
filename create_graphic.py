import json
import plotly.express as px
import pandas as pd
from datetime import datetime

# Load the data from the JSON file
with open('fake_users.json', 'r') as f:
    user_data = json.load(f)

# Convert the string datetime objects back to datetime
created_at_data = [datetime.strptime(user['created_at'], '%Y-%m-%d') for user in user_data]
updated_at_data = [datetime.strptime(user['updated_at'], '%Y-%m-%d') for user in user_data]

# Intertwine created_at and updated_at data
intertwined_data = []
for created, updated in zip(created_at_data, updated_at_data):
    intertwined_data.append({'Date': created, 'Type': 'Created At'})
    intertwined_data.append({'Date': updated, 'Type': 'Updated At'})

# Create a DataFrame with the intertwined data
df = pd.DataFrame(intertwined_data)

# Plot the histogram for the intertwined data
fig = px.histogram(df, x='Date', nbins=50, color='Type', title='Created At and Updated At Histogram')

# Show the graph
fig.show()