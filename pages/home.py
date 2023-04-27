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
                html.H1(children='MindPrint'),
            ]
        ),
        html.Div(
            className='subheader',
            children='Exploring the uniqueness of individuals\' brains.'
        )
    ]
)
