import dash
from dash import html, dcc

dash.register_page(__name__, order=2)

layout = html.Div(children=[
    html.H1(className='preproc_header', children='This is our PREPROCESSING page'),

    html.Div(className='preproc_header', children='''
        This is our PREPROCESSING page content.
    '''),

])