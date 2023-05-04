import dash
from dash import html, dcc

dash.register_page(__name__, order=2, location="sidebar")

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
            children="Editing Page"
        ),
        html.Div(
            className='mindprint-text',
            style={'font-size': '22px'},
            children=[
                html.P(
                    'The "Editing" page will be utilized at a later time when the Mind Print team is prepared. Its intended purpose is to facilitate the segmentation of streams and enable the simultaneous viewing of distinct data sets within the same time interval.'),
            ]
        )
    ]
)
