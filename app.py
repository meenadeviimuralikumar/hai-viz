from dash import Dash, html, dcc, Input, Output, callback, page_container
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Initialize the app
app = Dash(__name__, use_pages = True, suppress_callback_exceptions = True, external_stylesheets=external_stylesheets)


# App layout
app.layout = html.Div(children=[
    
    page_container
])


# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8051)