import dash
from dash import html, dcc

dash.register_page(__name__, order=3, location="sidebar")

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
            children="Preprocessing Page"
        ),
        html.Div(
            className='mindprint-text',
            style={'font-size': '22px'},
            children=[
                html.P(
                    'The "Preprocessing" page shall be employed at a later date when the Mind Print team deems it suitable for use. Its primary purpose is to facilitate the cleansing and refinement of data to enable the discovery of patterns and correlations within machine learning models.'),
            ]
        )
    ]
)
