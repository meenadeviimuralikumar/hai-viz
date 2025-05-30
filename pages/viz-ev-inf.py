import dash
from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Initialize the app
#app = Dash(__name__, use_pages = True, suppress_callback_exceptions = True, external_stylesheets=external_stylesheets)


dash.register_page(__name__, path="/ev-inf")

df = pd.read_csv("inf_evs.csv")

# App layout
layout = html.Div(children=[
    html.Br(),
    html.H4(style={'textAlign': 'center'}, children='Comparing Summary Informativeness across Article Types & Length'),
    html.P('INF  <- article_length + article_type + summary_length + news_reading_behavior', 
           style={'font-family':'monospace', 'color':'#4b7df0', 'display': 'flex', 'justifyContent': 'center', 'align-items': 'center'}),
    html.Div([html.P('For the above model, we will keep values of all other variables constant (at their mean or mode), and vary only the article type and length (significant effects)')],
           style={'width': '750px', 'text-align': 'center', 'margin-left':'325px'}),
    html.Br(),
    html.Div([
        html.Label('Select Article Type:', style={'margin-right': '10px'}),
        dcc.RadioItems(
            options = [
                {'label': 'Primary Reporting: Objective accounts from first hand investigation', 'value': 'Primary Reporting'},
                {'label': 'Secondary Reporting: Opinion based news, features, analyses, commentary', 'value': 'Secondary Reporting'}
            ],
            value='Primary Reporting',
            id='radio'),
    ], style={'display': 'flex', 'align-items': 'center', 'margin-left': '20px', 'margin-bottom': '20px'}),
    html.Br(),
    html.Div([html.Label('Adjust Article Length:', style={'margin-right': '10px'}), 
              dcc.Slider(900, 1200, step=1, value=1050,
                marks={
                    900: {'label': '900'},
                    1000: {'label': '1000'},
                    1100: {'label': '1100'},
                    1200: {'label': '1200'}
                },
                included = False,
                tooltip={"placement": "bottom", "always_visible": True}, 
                id='slider')],
             style = { 'display': 'inline-block', 'width':'50%'}),
    dcc.Graph(id="g1", config={'displayModeBar': False}, style={'textAlign': 'center', 'width': '700px'}) 
])

@callback(Output('g1', 'figure'), Input('slider', 'value'), Input('radio', 'value'))
def update_inf_viz(slider_value, radio_value):
    if(radio_value == 'Primary Reporting'):
        primary = 1
    else:
        primary = 0
   
    row_select = df[(df['primary_reporting'] == primary) & (df['article_length'] == slider_value)].reset_index(drop=True)

    #app.logger.info('Values')
    #app.logger.info(row_select['Strongly_Disagree']) 

    ev1 = round(row_select.loc[0, 'ev_sda'], 2)
    ev2 = round(row_select.loc[0, 'ev_da'], 2)
    ev3 = round(row_select.loc[0,'ev_n'], 2)
    ev4 = round(row_select.loc[0,'ev_a'], 2)
    ev5 = round(row_select.loc[0,'ev_sa'], 2)

    data = {'Likert Ratings': ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
        'Probability': [ev1, ev2, ev3, ev4, ev5],
        'Lower': [round(row_select.loc[0, 'upper_sda'], 2) - ev1, 
                       round(row_select.loc[0,'upper_da'], 2) - ev2,
                       round(row_select.loc[0,'upper_n'], 2) - ev3,
                       round(row_select.loc[0,'upper_a'], 2) - ev4,
                       round(row_select.loc[0,'upper_sa'], 2) - ev5],
        'Upper': [ev1 - round(row_select.loc[0, 'lower_sda'], 2), 
                       ev2 - round(row_select.loc[0,'lower_da'], 2),
                       ev3 - round(row_select.loc[0,'lower_n'], 2),
                       ev4 - round(row_select.loc[0,'lower_a'], 2),
                       ev5 - round(row_select.loc[0,'lower_sa'], 2)]}
    viz_df = pd.DataFrame(data)
    #app.logger.info('Break')
    #app.logger.info(viz_df['Likert Ratings'])
    #app.logger.info(viz_df['Probability'])

    fig = go.Figure(data=[go.Bar(x=viz_df['Likert Ratings'], 
                                 y=viz_df['Probability'],
                                 error_y=dict(
                                    type='data',
                                    symmetric=False, 
                                    array=viz_df['Upper'],
                                    arrayminus=viz_df['Lower'])   
                                 )])
    fig.update_yaxes(range=[0, 1])
    fig.update_layout(
        yaxis_title = "Probability of a User rating (X)",
        xaxis_title="Likert Rating (X)"
    )
    return fig


# Run the app
# if __name__ == '__main__':
#     app.run(debug=True, port=8051)
