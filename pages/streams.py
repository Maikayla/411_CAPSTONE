import dash
import dash_draggable
from dash import dcc, html
from MPapp import eeg_inst


dash.register_page(__name__, order=1, location="sidebar")

# Define the available streams in a list
available_streams = ['Fp1', 'Fp2', 'F3', 'F4', 'C3', 'C4', 'P3', 'P4', 'O1', 'O2', 'F7', 'F8',    'T7', 'T8', 'P7', 'P8', 'Fz', 'Cz',
                     'Pz', 'M1', 'M2', 'AFz', 'CPz', 'POz', 'AccX', 'AccY', 'AccZ', 'GyroX', 'GyroY', 'GyroZ', 'QuarW', 'QuarX', 'QuarY', 'QuarZ']

# Define the layout
layout = html.Div(children=[
    # Tabbed Menu
    dcc.Tabs(
        id="tabs-with-classes",
        value='tab-1',
        parent_className='slate',
        className='slate',
        children=[
            dcc.Tab(
                label='Choose Streams',
                value='tab-1',
                className='slate',
                children=[
                    html.Div(children=[
                        html.Div(id='output_data'),
                        html.Div(id="hidden-search-value",
                                 style={"visibility": "hidden"}),
                        html.Button('Create', id='create_card_button',
                                    n_clicks=0, className='slate'),
                        dcc.Dropdown(
                            options=[{'label': s, 'value': s}
                                     for s in available_streams],
                            placeholder='Select streams:',
                            id='select_stream_dropdown',
                            multi=True
                        )
                    ]),

                    html.Div([
                        dash_draggable.GridLayout(
                            id='dd-output-container',
                            children=[
                                dcc.Graph(
                                    figure=eeg_inst.graphStream(
                                        "Neighborhood 1", available_streams[:6])
                                )
                            ]
                        )
                    ])
                ]
            ),
            dcc.Tab(
                label='2D Heat Map',
                value='tab-2',
                className='slate',
                children=[
                    html.Div([
                        html.H3('2D Heatmap needs to be fixed')
                    ])
                ]
            ),
            dcc.Tab(
                label='All Streams',
                value='tab-3',
                className='slate',
                children=[
                    html.Div([
                        # dcc.Graph(figure=theplotiactuallycareabout),
                    ])
                ]
            ),
        ]
    ),

    html.Div(id='tabs-content-classes'),
])
