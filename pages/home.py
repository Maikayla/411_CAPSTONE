import dash
from dash import html, dcc

dash.register_page(__name__, path='/')

layout =html.Div(
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
])