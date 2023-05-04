import dash
from dash import html, dcc

dash.register_page(__name__, order=3, location = "sidebar")

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
            style={'font-weight': 'bold', 'font-size': '20px', 'text-align': 'center'},
            children="Preprocessing Page"
        ),
        html.Div(
            className='mindprint-text',
            style={'font-size': '16px'},
            children=[
                html.P('This preprocessing page will be used in the future once the Mind Print team is ready for it. It will be used to:'),
                html.P(
                    '- Clean and prepare data for use in finding trends in machine learning models')
            ]
        )
    ]
)