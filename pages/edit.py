import dash
from dash import html, dcc

dash.register_page(__name__, order=2, location = "sidebar")

layout = html.Div(children=[
    html.H1(className='edit_header', children='This is our EDITING page'),

    html.Div(className='edit_header', children='''
        This is our EDITING page content.
    '''),

])