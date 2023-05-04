import dash
from dash import html, dcc

dash.register_page(__name__, order=4, location="sidebar")

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
            style={'font-weight': 'bold',
                   'font-size': '24px', 'text-align': 'center'},
            children="Detecting Patterns Page"
        ),
        html.Div(
            className='mindprint-text',
            style={'font-size': '22px'},
            children=[
                html.P(
                    'The "Detecting Patterns" page will be utilized by the Mind Print team in the future, once it is deemed ready. Its purpose will be to employ advanced machine learning models to identify any discernible patterns within streams of data surrounding events or stimuli.'),
            ]
        )
    ]
)
