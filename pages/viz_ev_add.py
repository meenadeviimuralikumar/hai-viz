import dash
from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Initialize the app
#app = Dash(__name__, external_stylesheets=external_stylesheets)

df_add = pd.read_csv("add_all.csv")


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
        html.P('article_length = 1005 words, article_type = Primary Reporting, summary_length = 97 words'),
    ], style={'color':'#4b7df0', 'font-family':'monospace', 'display': 'flex', 'justifyContent': 'center', 'align-items': 'center', 'padding': '20px'}),
    html.Div([
        html.Label('Select News Reading Behavior:', style={'margin': '15px'}),
        dcc.Checklist(
            ['Tracker', 'Reviewer', 'Conversationalist'],
            ['Tracker', 'Reviewer', 'Conversationalist'],
            inline = True,
            id = 'check'
        ),
    ], style={'display': 'flex', 'align-items': 'center', 'margin-left': '420px', 'margin-bottom': '20px'}),    
    html.Div([
            html.H3('ADD'),
            html.P('The original source offered valuable additional context'),
            html.Br(),
            dcc.Graph(id='g1', config={'displayModeBar': False})
        ], style={'width': '900px'})
    ])

@callback(Output('g1', 'figure'), Input('check', 'value'))
def update_viz(checkbox_values):

    selected = [cat.lower() for cat in checkbox_values]

    df2 = df_add[df_add['behavior'].isin(selected)]

    fig2 = go.Figure()


    if(len(checkbox_values) > 1):

        fig2 = px.bar(df2, x="rating", y="probability",
                 color="behavior", 
                 barmode='group',
                 color_discrete_map={'tracker': '#6ACDFF', 'conversationalist': '#FF9898', 'reviewer': '#95D86E'},
                 error_y=df2['97.50%'] - df2['probability'], 
                 error_y_minus= df2['probability'] - df2['2.50%'])

    elif(len(selected) == 1):
        if(selected[0]) == 'tracker':
            col = '#6ACDFF'
        elif(selected[0] == 'reviewer'):
            col = '#95D86E'
        else:
            col = '#FF9898'
        fig2 = px.bar(df2, x="rating", y="probability",
                 color_discrete_sequence=[col],
                 error_y=df2['97.50%'] - df2['probability'], 
                 error_y_minus= df2['probability'] - df2['2.50%'])
        fig2.update_layout(showlegend = True)
        
    fig2.update_traces(error_y_color='gray', error_y_thickness=1)
    fig2.update_layout(yaxis_range=[0, 1])
    fig2.update_layout(
        yaxis_title = "Probability of a User rating X",
        xaxis_title="X",
        showlegend = True
    )
    return fig2

# Run the app
# if __name__ == '__main__':
#     app.run(debug=True)