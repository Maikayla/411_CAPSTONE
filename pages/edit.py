import dash
from dash import html, dcc

dash.register_page(__name__, order=2, location = "sidebar")

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
            style={'font-weight': 'bold', 'font-size': '70px', 'text-align': 'center'},
            children="Editing Page."
        ),
        html.Div(
            className='mindprint-text',
            style={'font-size': '16px'},
            children=[
                html.P('This editing page will be used in the future once the Mind Print team is ready for it. They will use it to:'),
                html.P(
                    '- Editing Reason Number 1.'),
                html.P(
                    '- Editing Reason Number 2.'),
                html.P(
                    '- Editing Reason Number 3.')
            ]
        )
    ]
)