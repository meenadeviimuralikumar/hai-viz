import dash
from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Initialize the app
#app = Dash(__name__, external_stylesheets=external_stylesheets)

#df_add = pd.read_csv("add_all.csv")


dash.register_page(__name__, path="/ev-add")

# Define the layout (a Div with a Graph)
layout = html.Div([
    html.Br(),
    html.H4(style={'textAlign': 'center'}, children='How did different kinds of news readers rate the ADD attribute?'),
    html.P('ADD  <- article_length + article_type + summary_length + news_reading_behavior', 
           style={'font-family':'monospace', 'color':'#4b7df0', 'display': 'flex', 'justifyContent': 'center', 'align-items': 'center'}),
    html.Div([html.P('For the above model, we will keep values of all other variables constant (at their mean or mode), and vary the news reading behavior')],
           style={'width': '750px', 'text-align': 'center', 'margin-left':'325px'}),
    html.Div([
        html.Pre('[Current]  P(A) => 1005 words + Primary Reporting + 97 words +  '),
        dcc.Dropdown(
            id='add-pre',
            options=[
                {'label': 'Conversationalist', 'value': 'Conversationalist'},
                {'label': 'Reviewer', 'value': 'Reviewer'},
                {'label': 'Tracker', 'value': 'Tracker'}
            ],
        value='Conversationalist',
        style={'width': '200px'}
        )
    ], style={'color':'#4b7df0', 'font-family':'monospace', 'display': 'flex', 'justifyContent': 'center', 'align-items': 'center', 'padding': '20px'}),
    html.Div([
        html.Pre('[What-If]  P(B) => 1005 words + Primary Reporting + 97 words +  '),
        dcc.Dropdown(
            id='add-post',
            options=[
                {'label': 'Conversationalist', 'value': 'Conversationalist'},
                {'label': 'Reviewer', 'value': 'Reviewer'},
                {'label': 'Tracker', 'value': 'Tracker'}
            ],
        value='Conversationalist',
        style={'width': '200px'}
        )
    ], style={'color':'#4b7df0', 'font-family':'monospace', 'display': 'flex', 'justifyContent': 'center', 'align-items': 'center', 'padding': '20px'}),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div(id="contingency-table"),
    html.Br(),
    html.Br(),
    html.Br(),
    html.P('(Greyed out text ndicates non-significant effect as the interval contains 0 or 1 respectively)', style={'color': '#C0C0C0', 'font-size': '14px', 'text-align': 'center'})
    ])

@callback(Output('contingency-table', 'children'), Input('add-pre', 'value'),  Input('add-post', 'value'))
def update_ev_add_viz(addpre, addpost):


    columns = ['', 'Absolute Difference[P(B) - P(A)]', 'Relative Difference [P(B) / P(A)]']
    header = html.Tr([html.Th(col, style={"padding": "12px"}) for col in columns])

    if(addpre == addpost):

        rows = [
            html.Tr([html.Td('Strongly Disagree/Disagree', style={"padding": "8px"})] +
                [html.Td(0, style={"padding": "8px"})] +
                [html.Td(1, style={"padding": "8px"})]),
            html.Tr([html.Td('Neutral', style={"padding": "8px"})] +
                [html.Td(0, style={"padding": "8px"})] +
                [html.Td(1, style={"padding": "8px"})]),
            html.Tr([html.Td('Agree/Strongly Agree', style={"padding": "8px"})] +
                [html.Td(0, style={"padding": "8px"})] +
                [html.Td(1, style={"padding": "8px"})])
        ]

        return html.Table([header] + rows, style={"border-collapse": "collapse",'margin-left': 'auto', 'margin-right': 'auto'})

    if(addpre != addpost):
        full_df = pd.read_csv("concat_add.csv")
        full_df = full_df.round(2)

        pre = ''
        post = ''

        if(addpre == 'Conversationalist'):
            pre = 'convo'
            if(addpost == 'Reviewer'):
                post = 'reviewer'
            else:
                post = 'tracker'

        if(addpre == 'Reviewer'):
            pre = 'reviewer'
            if(addpost == 'Conversationalist'):
                post = 'convo'
            else:
                post = 'tracker'
        
        if(addpre == 'Tracker'):
            pre = 'tracker'
            if(addpost == 'Conversationalist'):
                post = 'convo'
            else:
                post = 'reviewer'
             

        df = full_df[full_df['pre'] == pre]
        df = df[df['post'] == post]

        ratings = ['sda_da', 'n', 'a_sa']
        row_list = []
        y = []

        for x in range(3):

            ddf = df[df['rating'] == ratings[x]]

            fd = ddf.loc[ddf['measure'] == 'fd', 'prob'].iloc[0]
            fd_low = fd - ddf.loc[ddf['measure'] == 'fd', 'lower'].iloc[0]
            fd_up = ddf.loc[ddf['measure'] == 'fd', 'upper'].iloc[0] - fd


            rr = ddf.loc[ddf['measure'] == 'rr', 'prob'].iloc[0]
            rr_low = rr - ddf.loc[ddf['measure'] == 'rr', 'lower'].iloc[0]
            rr_up = ddf.loc[ddf['measure'] == 'rr', 'upper'].iloc[0] - rr 

            fd = fd.round(2)
            fd_low = fd_low.round(2)
            fd_up = fd_up.round(2)

            rr = rr.round(2)
            rr_low = rr_low.round(2)
            rr_up = rr_up.round(2)

            if(fd-fd_low <= 0 <= fd+fd_up):
                y.append(x*2)

            if(rr-rr_low <= 1 <= rr+rr_up):
                y.append(x*2 + 1)
            
            fd = f"{fd} (+{fd_up} / -{fd_low})"
            rr = f"{rr} (+ {rr_up} / - {rr_low})"
            row_list.append(fd)
            row_list.append(rr)

        rows = [
            html.Tr([html.Td('Strongly Disagree/Disagree', style={"padding": "8px"})] +
                [html.Td(row_list[0], style={"color": "#C0C0C0","padding": "8px"} if 0 in y else {"padding": "8px"})] +
                [html.Td(row_list[1], style={"color": "#C0C0C0","padding": "8px"} if 1 in y else {"padding": "8px"})]),
            html.Tr([html.Td('Neutral', style={"padding": "8px"})] +
                [html.Td(row_list[2], style={"color": "#C0C0C0","padding": "8px"} if 2 in y else {"padding": "8px"})] +
                [html.Td(row_list[3], style={"color": "#C0C0C0","padding": "8px"} if 3 in y else {"padding": "8px"})]),
            html.Tr([html.Td('Agree/Strongly Agree', style={"padding": "8px"})] +
                [html.Td(row_list[4], style={"color": "#C0C0C0","padding": "8px"} if 4 in y else {"padding": "8px"})] +
                [html.Td(row_list[5], style={"color": "#C0C0C0","padding": "8px"} if 5 in y else {"padding": "8px"})])
        ]

        return html.Table([header] + rows, style={"border-collapse": "collapse",'margin-left': 'auto', 'margin-right': 'auto'})

        

# Run the app
# if __name__ == '__main__':
#     app.run(debug=True)
