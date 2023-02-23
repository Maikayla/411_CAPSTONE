from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

app = Dash(__name__)

app.layout = html.Div(
    className='bar',
    children=[

        # Header
        html.H1(
            className='header',
            children='MindPrint',
        ),

        # SubHeader
        html.Div(
            className='subHeader',
            children='''Exploring the uniqueness of individuals' brains.''',
        ),

        # Tabbed Menu
        dcc.Tabs(
            id="tabs-with-classes",
            value='tab-2',
            parent_className='custom-tabs',
            className='custom-tabs-container',
            children=[
                dcc.Tab(
                    label='Tab One',
                    value='tab-1',
                    className='custom-tab',
                    selected_className='custom-tab--selected'
                ),
                dcc.Tab(
                    label='Tab Two',
                    value='tab-2',
                    className='custom-tab',
                    selected_className='custom-tab--selected'
                ),
                dcc.Tab(
                    label='Tab Three',
                    value='tab-3', className='custom-tab',
                    selected_className='custom-tab--selected'
                ),
                dcc.Tab(
                    label='Tab Four',
                    value='tab-4',
                    className='custom-tab',
                    selected_className='custom-tab--selected'
                ),
            ]),
        html.Div(id='tabs-content-classes')
    ])


@app.callback(Output('tabs-content-classes', 'children'),
              Input('tabs-with-classes', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Tab content 1')
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2')
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H3('Tab content 3')
        ])
    elif tab == 'tab-4':
        return html.Div([
            html.H3('Tab content 4')
        ])


if __name__ == '__main__':
    app.run_server(debug=True)
