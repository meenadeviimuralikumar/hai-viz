import dash
from dash import html

dash.register_page(__name__, path="/")  

layout = html.Div([
    html.H2(style={'textAlign': 'center'}, children = 'Interactive Visualization of Data from Human-AI Evaluations'),
    html.Br(),
    html.H6('How might we leverage to AI-generated news summaries to reimagine digital news consumption?'),
    html.P('Could we design for responsible, accessible, and less stressful ways for engaging with news?',
           style={'textIndent':'40px'}),
    html.Br(),
    html.P('Evaluating AI-generated news summaries against the original news article to ensure they do not contain factual errors or hallucinations is an important first step. Human feedback on these summaries are also helpful and overcomes limitations of automatic evaluation. To that end we have some data from news readers:-'),
    html.Div([
        html.Img(src = '/assets/studyproc.jpg' , alt = "Study Procedure", width='700px')], 
        style={'text-align': 'center'}),
    html.P('In the post-task survey, the following statements were presented and users provided a Likert Rating (1-Strongly Disagree to 5-Strongly Agree)'),
    html.Ul([html.Li('Informative - The summary covered the key points of the news article.'), 
             html.Li('Surrogate - The summary captured the article well enough to act as a stand-in.'), 
             html.Li('Additional Context -  While the summary provided an overview, engaging with the original source offered valuable additional context.')])
])