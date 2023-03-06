import dash
from dash import html, dcc

dash.register_page(__name__, order=4)

layout = html.Div(children=[
    html.H1(className='pattern_header', children='This is our DETECTING PATTERNS page'),

    html.Div(className='pattern_header', children='''
        This is our DETECTING PATTERNS page content.
    '''),

])