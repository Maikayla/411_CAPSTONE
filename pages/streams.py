import dash
from dash import html, dcc

dash.register_page(__name__, location = "sidebar")

layout = html.Div(children=[
    html.H1(className='streams_header', children='This is our Streams page'),

    html.Div(children=[
        # Tabbed Menu
        dcc.Tabs(
            id="tabs-with-classes",
            value='tab-1',
            parent_className='custom-tabs',
            className='custom-tabs-container',
            children=[

                dcc.Tab(
                    label='Single Streams',
                    value='tab-1',
                    className='custom-tab',
                    selected_className='custom-tab--selected'
                ),
                dcc.Tab(
                    label='2D Heat Map',
                    value='tab-2',
                    className='custom-tab',
                    selected_className='custom-tab--selected'
                ),
                dcc.Tab(
                    label='More Streams',
                    value='tab-3', className='custom-tab',
                    selected_className='custom-tab--selected'
                ),
                #dcc.Tab(
                #    label='Nothing for now...',
                #    value='tab-4',
                #    className='custom-tab',
                #    selected_className='custom-tab--selected'
                #),
            ]),

        html.Div(id='tabs-content-classes'),

    ]),

])