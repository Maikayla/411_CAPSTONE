import dash
from dash import html, dcc

dash.register_page(__name__, order=1, location = "sidebar")

layout = html.Div(children=[
    html.H1(className='slate', children='View Raw Streams'),

    html.Div(children=[
        # Tabbed Menu
        dcc.Tabs(
            id="tabs-with-classes",
            value='tab-1',
            parent_className='slate',
            className='slate',
            children=[

                dcc.Tab(
                    label='Single Streams',
                    value='tab-1',
                    className='slate'
                ),
                dcc.Tab(
                    label='2D Heat Map',
                    value='tab-2',
                    className='slate',
                ),
                dcc.Tab(
                    label='More Streams',
                    value='tab-3', 
                    className='slate',
                ),
                #dcc.Tab(
                #    label='Nothing for now...',
                #    value='tab-4',
                #    className='slate',
                #),
            ]),

        html.Div(id='tabs-content-classes'),

    ]),

])