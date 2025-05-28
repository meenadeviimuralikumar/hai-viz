import dash
from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# # Initialize the app
# app = Dash(__name__, external_stylesheets=external_stylesheets)

dash.register_page(__name__, path="/fdrr-surr")


fd_df = pd.read_csv("surr_all.csv")
rr_df = pd.read_csv("add_all.csv")

# App layout
layout = html.Div(children=[
    html.Br(),
    html.H4(style={'textAlign': 'center'}, children='Comparing SURR ratings between different News Reading Behaviors'),
    html.Br(),
    html.Div([html.P('[SURR] The summary captured the article well enough to act as a surrogate.')],
           style={'width': '850px', 'text-align': 'center', 'margin-left':'325px'}),
    html.P('SURR  <- article_length + article_type + summary_length + news_reading_behavior', 
           style={'font-family':'monospace', 'color':'#4b7df0', 'display': 'flex', 'justifyContent': 'center', 'align-items': 'center'}),
    html.Div([html.P('For the above model, we will simulate changes in SURR ratings by only changing the news reading behavior and keeping values of all other variables constant (at their mean or mode).')],
           style={'width': '750px', 'text-align': 'center', 'margin-left':'325px'}),
    html.Div([
        html.P('[Pre-] 1005 words + Primary Reporting + 97 words +  '),
        dcc.Dropdown(
            id='dd-pre',
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
        html.P('[Post-] 1005 words + Primary Reporting + 97 words +  '),
        dcc.Dropdown(
            id='dd-post',
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
    #html.P(style={'textAlign': 'center'}, id = 'statement', children=''),
    html.Div([
        html.Div([
            dcc.Graph(id='graph1', config={'displayModeBar': False})
        ], className="six columns"),

        html.Div([
            dcc.Graph(id='graph2', config={'displayModeBar': False})
        ], className="six columns"),
    ],  style={'margin-left': '25px'}, className="row"),
    html.Ul([html.Li('-Indicates a non-significant effect as it crosses the 0 or 1x line.')],
            className="custom-list", style = {'display': 'flex', 'justifyContent': 'center', 'align-items': 'center'}),
    html.Br()
])

# @callback(Output('statement', 'children'), Input('dd', 'value'))
# def update_output(value):
#     return f'Comparing ratings of a {value} to other behaviors'


@callback(Output('graph1', 'figure'), Output('graph2', 'figure'), Input('dd-pre', 'value'),  Input('dd-post', 'value'))
def update_viz(ddpre, ddpost):

    fig1 = go.Figure()
    fig2 = go.Figure()

    x_range = [0.1, 4]
    fd_x_range = [-0.6, 0.6]

    if(ddpost == 'Reviewer'):
        df1 = pd.read_csv("surr_fd_reviewer.csv")
        df2 = pd.read_csv("surr_rr_reviewer.csv")

        if(ddpre == 'Conversationalist'):
            df1 = df1[df1['comp'] == 'convo']
            df1 = df1.round(2)

            df2 = df2[df2['comp'] == 'convo']
            df2 = df2.round(2)

            title1 = 'Difference in Probabilities (Reviewer <- Conversationalist ratings)'
            title2 = 'Ratio of Probabilities (Reviewer <- Conversationalist ratings)'

            fd_color = 'tomato'
            rr_color = 'darkviolet'

            fd_color_list = ['tomato','tomato', 'tomato']
            rr_color_list = ['darkviolet','darkviolet', 'darkviolet']

        elif(ddpre == 'Tracker'):
            df1 = df1[df1['comp'] == 'tracker']
            df1 = df1.round(2)

            df2 = df2[df2['comp'] == 'tracker']
            df2 = df2.round(2)

            title1 = 'Difference in Probabilities (Reviewer <- Tracker ratings)'
            title2 = 'Ratio of Probabilities (Reviewer <- Tracker ratings)'

            fd_color = 'tomato'
            rr_color = 'darkviolet'

            fd_color_list = ['tomato','tomato', 'tomato']
            rr_color_list = ['darkviolet','darkviolet', 'darkviolet']

            fd_x_range = [-0.7, 0.7]
            x_range = [0.05, 5]

        else:
            df1 = df1[df1['comp'] == 'reviewer']
            df1 = df1.round(2)

            df2 = df2[df2['comp'] == 'reviewer']
            df2 = df2.round(2)

            title1 = 'Difference in Probabilities (Reviewer <- Reviewer ratings)'
            title2 = 'Ratio of Probabilities (Reviewer <- Reviewer ratings)'

            fd_color = 'black'
            rr_color = 'black'

            fd_color_list = ['black','black', 'black']
            rr_color_list = ['black','black', 'black']
            

    elif(ddpost == 'Tracker'):
        
        df1 = pd.read_csv("surr_fd_tracker.csv")
        df2 = pd.read_csv("surr_rr_tracker.csv")

        if(ddpre == 'Conversationalist'):
            df1 = df1[df1['comp'] == 'convo']
            df1 = df1.round(2)

            df2 = df2[df2['comp'] == 'convo']
            df2 = df2.round(2)

            title1 = 'Difference in Probabilities (Tracker <- Conversationalist ratings)'
            title2 = 'Ratio of Probabilities (Tracker <- Conversationalist ratings)'

            fd_color = 'tomato'
            rr_color = 'darkviolet'

            fd_color_list = ['tomato','black', 'tomato']
            rr_color_list = ['darkviolet','black', 'darkviolet']

        elif(ddpre == 'Reviewer'):
            df1 = df1[df1['comp'] == 'reviewer']
            df1 = df1.round(2)

            df2 = df2[df2['comp'] == 'reviewer']
            df2 = df2.round(2)

            title1 = 'Difference in Probabilities (Tracker <- Reviewer ratings)'
            title2 = 'Ratio of Probabilities (Tracker <- Reviewer ratings)'

            fd_color = 'tomato'
            rr_color = 'darkviolet'

            fd_color_list = ['tomato','tomato', 'tomato']
            rr_color_list = ['darkviolet','darkviolet', 'darkviolet']

            fd_x_range = [-0.7, 0.7]
            x_range = [0.1, 10]
        
        else:
            df1 = df1[df1['comp'] == 'tracker']
            df1 = df1.round(2)

            df2 = df2[df2['comp'] == 'tracker']
            df2 = df2.round(2)

            title1 = 'Difference in Probabilities (Tracker <- Tracker ratings)'
            title2 = 'Ratio of Probabilities (Tracker <- Tracker ratings)'

            fd_color = 'black'
            rr_color = 'black'

            fd_color_list = ['black','black', 'black']
            rr_color_list = ['black','black', 'black']
    
    else:

        df1 = pd.read_csv("surr_fd_convo.csv")
        df2 = pd.read_csv("surr_rr_convo.csv")

        if(ddpre == 'Tracker'):
            df1 = df1[df1['comp'] == 'tracker']
            df1 = df1.round(2)

            df2 = df2[df2['comp'] == 'tracker']
            df2 = df2.round(2)

            title1 = 'Difference in Probabilities (Conversationalist <- Tracker ratings)'
            title2 = 'Ratio of Probabilities (Conversationalist <- Tracker ratings)'

            fd_color = 'tomato'
            rr_color = 'darkviolet'

            fd_color_list = ['tomato','black', 'tomato']
            rr_color_list = ['darkviolet','black', 'darkviolet']

        elif(ddpre == 'Reviewer'):
            df1 = df1[df1['comp'] == 'reviewer']
            df1 = df1.round(2)

            df2 = df2[df2['comp'] == 'reviewer']
            df2 = df2.round(2)

            title1 = 'Difference in Probabilities (Conversationalist <- Reviewer ratings)'
            title2 = 'Ratio of Probabilities (Conversationalist <- Reviewer ratings)'

            fd_color = 'tomato'
            rr_color = 'darkviolet'

            x_range = [0.1, 7]

            fd_color_list = ['tomato','tomato', 'tomato']
            rr_color_list = ['darkviolet','darkviolet', 'darkviolet']
        
        else:
            df1 = df1[df1['comp'] == 'convo']
            df1 = df1.round(2)

            df2 = df2[df2['comp'] == 'convo']
            df2 = df2.round(2)

            title1 = 'Difference in Probabilities (Conversationalist <- Conversationalist ratings)'
            title2 = 'Ratio of Probabilities (Conversationalist <- Conversationalist ratings)'

            fd_color = 'black'
            rr_color = 'black'

            fd_color_list = ['black','black', 'black']
            rr_color_list = ['black','black', 'black']

    fig1.add_trace(go.Scatter(
        x = df1['FD'],
        y = df1['dummy_y'],
        mode='markers',
        marker=dict(size=12, color = fd_color_list),
        hoverinfo='skip'
    ))
    fig1.add_trace(go.Scatter(
        x = df1['FD'],
        y = df1['dummy_y'],
        error_x = dict(
        type = 'data',
        symmetric = False,
        array = df1['97.50%'] - df1['FD'],
        arrayminus = df1['FD'] - df1['2.50%'],
        thickness=1.2,
        color = fd_color
        ),
        mode='markers',
        marker=dict(
            size=10,
            opacity=0,
            color = fd_color
            ),
            showlegend=False
    ))
        
    fig1.update_layout(
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        showlegend=False,
        hoverlabel=dict(
            bgcolor = 'white',
            font_color= 'black'
            ),
            title = dict(
                text = title1,
                font=dict(size=14)
            ),
            yaxis = dict(
                tickvals = [3, 2, 1],
                ticktext =['Strongly Disagree+Disagree', 'Neutral', 'Strongly Agree+Agree']
            )
        )
    fig1.update_xaxes(range = fd_x_range)
    # fig1.add_shape(
    #     type="line",
    #     x0=1, y0=0, x1=1, y1=2.5,
    #     line=dict(color="darkgrey", width=1, dash="dash")
    # )

    fig2.add_trace(go.Scatter(
        x = df2['RR'],
        y = df2['dummy_y'],
        mode='markers',
        marker=dict(size=12, color = rr_color_list),
        hoverinfo='skip'
    ))
    fig2.add_trace(go.Scatter(
        x = df2['RR'],
        y = df2['dummy_y'],
        error_x = dict(
            type = 'data',
            symmetric = False,
            array = df2['97.50%'] - df2['RR'],
            arrayminus = df2['RR'] - df2['2.50%'],
            thickness=1.2,
            color = rr_color
            ),
            mode='markers',
            marker=dict(
                size=10,
                opacity=0,
                color = rr_color
                ),
            showlegend=False
    ))
    fig2.update_layout(
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        showlegend=False,
        hoverlabel=dict(
            bgcolor = 'white',
            font_color= 'black'
            ),
        title = dict(
                text = title2,
                font=dict(size=14)
            ),
        xaxis = dict(
            tickvals = [0.1, 0.5, 1, 2, 3, 4, 5, 6, 7, 8, 10],
            ticktext = ['0.1x','0.5x', '1x', '2x', '3x', '4x', '5x', '6x', '7x', '8x','10x']
            ),
        yaxis = dict(
            tickvals = [3, 2, 1],
            ticktext =['Strongly Disagree+Disagree', 'Neutral', 'Strongly Agree+Agree']
            )
        )
    fig2.update_xaxes(range = x_range)
    fig2.add_shape(
        type="line",
        x0=1, y0=0, x1=1, y1=4,
        line=dict(color="darkgrey", width=1, dash="dash")
    )


    return fig1, fig2
    


# Run the app
# if __name__ == '__main__':
#     app.run(debug=True, port=8051)