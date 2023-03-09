import dash
from dash import html, dcc

dash.register_page(__name__, path='/')

layout = html.Div(children=[
    html.H1(className='home_header', children='This is our Home page'),

    html.Div(className='home_header', children='''
        This is our Home page content.
    '''),

    # html.Div(
    #     className='bar',
    #     children=[

    #         # Header
    #         html.H1(
    #             className='header',
    #             children='MindPrint',
    #         ),

    #         # SubHeader
    #         html.Div(
    #             className='subHeader',
    #             children='''Exploring the uniqueness of individuals' brains.''',
    #         ),
    #     ])

])