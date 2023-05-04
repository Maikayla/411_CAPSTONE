import dash
from dash import html, dcc

dash.register_page(__name__, order=4, location = "sidebar")

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
            children="Detecting Patterns Page"
        ),
        html.Div(
            className='mindprint-text',
            style={'font-size': '16px'},
            children=[
                html.P('This detecting patterns page will be used in the future once the Mind Print team is ready for it. It will be used to:'),
                html.P(
                    '- Utilize machine learning models to detect any patterns in the streams around events (stimuli)')
            ]
        )
    ]
)