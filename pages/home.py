import dash
from dash import html, dcc

dash.register_page(__name__, path='/')

layout = html.Div(
    className='container',
    children=[
        html.Div(
            className='header',
            children=[
                html.Img(
                    src='/assets/logo.png',
                    className='logo'
                ),
            ]
        ),
        html.Div(
            className='subheader',
            children='Exploring the uniqueness of individuals\' brains.'
        ),
        html.Div(
            className='mindprint-text',
            children=[
                html.P('MindPrint is a research project at SELU, headed by Dr. Ömer Soysal that explores uniqueness of individuals’ brain signals and aims to:'),
                html.Ul([
                    html.Li(
                        'Develop a system to explore specific characteristics of individuals’ brain signals'),
                    html.Li(
                        'Build and implement a curriculum to train the workforce for computational aspects of brain signals')
                ])
            ]
        )
    ]
)
