import dash
from dash import html, dcc
import dash_draggable
from MPapp import eeg_inst

dash.register_page(__name__, order=1, location = "sidebar")


layout = html.Div(children=[
    html.Div(children=[
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
                     children= [ 
                             html.Div(children =[
                                html.Div(id='output_data'),
                                dcc.Input(id='input_card_title', type="text", placeholder="Enter Title", debounce=True),
                                html.Button('Create', id= 'create_card_button', n_clicks=0, className='slate'),
                                html.Br(),
                                dcc.Dropdown(['Fp1', 'Fp2', 'F3', 'F4', 'C3', 'C4', 'P3', 'P4', 'O1', 'O2', 'F7', 'F8', 'T7',
                                            'T8', 'P7', 'P8', 'Fz', 'Cz', 'Pz', 'M1', 'M2', 'AFz', 'CPz', 'POz', 'AccX', 'AccY',
                                             'AccZ', 'GyroX', 'GyroY', 'GyroZ', 'QuarW', 'QuarX', 'QuarY', 'QuarZ'], placeholder='Select streams:', id='select_stream_dropdown', multi=True)
                             ]),

                            html.Div([ 
                                dash_draggable.GridLayout(id='dd-output-container', children=[
                                        #dcc.Graph(figure = eeg_inst.graphStream( "Neighborhood 1", ['Fp1', 'Fp2', 'F3', 'F4', 'C3', 'C4'])),
                                    ]
                                ),
                                html.Div(id="hidden-search-value", style={"visibility":"hidden"}),
                            ])
                    ]
                ),
                dcc.Tab(
                    label='2D Heat Map',
                    value='tab-2',
                    className='slate',
                    children= [
                            html.Div([
                                html.H3('2D Heatmap needs to be fixed')
                            ])
                    ]
                ),
                dcc.Tab(
                    label='All Streams',
                    value='tab-3', 
                    className='slate',
                    children= [
                        html.Div([
                            #dcc.Graph(figure=theplotiactuallycareabout),
                        ])
                    ]
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