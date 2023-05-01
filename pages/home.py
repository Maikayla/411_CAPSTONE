import dash
from dash import html, dcc

dash.register_page(name, path='/')

layout = html.Div(
    style={'text-align': 'center'},
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
            style={'font-weight': 'bold', 'font-size': '20px'},
            children="Exploring the uniqueness of individuals' brains"
        ),
        html.Div(
            className='mindprint-text',
            style={'font-size': '16px'},
            children=[
                html.P('MindPrint is a research project at SELU, headed by Dr. Ömer Soysal that explores uniqueness of individuals’ brain signals and aims to:'),
                html.P(
                    '- Develop a system to explore specific characteristics of individuals’ brain signals'),
                html.P(
                    '- Build and implement a curriculum to train the workforce for computational aspects of brain signals')
            ]
        )
    ]
)
