from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
} #end colors

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(children='MindPrint',
            style={
            'textAlign': 'center',
            'color': colors['text']
            }),

    html.Div(children='''
        Exploring the uniqueness of individuals' brains.
    ''', style={
        'textAlign': 'center',
        'color': colors['text']
        }),


        ##  ##
    ## TABBED MENU ##
        ##  ##
    dcc.Tabs(id="tabs-example-graph", value='tab-1-example-graph', children=[
        dcc.Tab(label='Tab One', value='tab-1-example-graph'),
        dcc.Tab(label='Tab Two', value='tab-2-example-graph'),
    ]),
    html.Div(id='tabs-content-example-graph')

])

if __name__ == '__main__':
    app.run_server(debug=True)
