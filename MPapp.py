from dash import Dash, html, dcc
import dash
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, ClientsideFunction 
import dash_bootstrap_components as dbc

#######################################

import FileReader
import DataVisualization
import mne
import mpld3
filereader = FileReader.FileReader()
filereader.setRawData()

filereader.setDataFrame()


eeg_inst = DataVisualization.DataVisualization(
    filereader.raw_data, filereader.raw_df, filereader.marker_stream, filereader.markers_codes, filereader.info)

###

#######################################
app = Dash(__name__, use_pages=True, external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/dragula/3.7.2/dragula.min.js"],  external_stylesheets=[dbc.themes.SLATE, dbc.icons.FONT_AWESOME],)

# TODO FIX THE 2d Heatmap
container_2dHeatmap = eeg_inst.get_2dHeatmap_child(app)

singlestreamsplot = eeg_inst.graphSingleStreams(
    'Title of My Single Streams\n Plotly Graph Object', eeg_inst.raw_df.columns[0:5])
othersinglestreamsplot = eeg_inst.graphSingleStreams(
    'Another Single Streams Plot', eeg_inst.raw_df.columns[:])
theplotiactuallycareabout = eeg_inst.graphStream('Wow, what a plotly plot for plotting', ["Fp1", "Fp2", "F3", "F4", "O2"])


#Sidebar navigation - REFERENCE: https://community.plotly.com/t/sidebar-with-icons-expands-on-hover-and-other-cool-sidebars/67318
sidebar = html.Div(
    [
        html.Div(
            [
                html.H2("Menu", style={"color": "blue"}),
            ],
            className="sidebar-header",
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    [html.I(className="fas fa-home me-2"), html.Span("Home")],
                    href="/",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-calendar-alt me-2"),
                        html.Span("Streams"),
                    ],
                    href="/streams",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-pen-nib"),
                        html.Span("Edit"),
                    ],
                    href="/edit",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-sliders"),
                        html.Span("Preprocessing"),
                    ],
                    href="/preprocessing",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-chess-board"),
                        html.Span("Detecting Patterns"),
                    ],
                    href="/detect-patterns",
                    active="exact",
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar",
)


app.layout = html.Div([ 

    sidebar,
    html.Div(
            [
                dash.page_container
            ],
            className="content",
        ),
])

app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name = "make_draggable"),
    Output("drag_container","data-drag"),
    [Input("drag_container","id")],
)

# NOTE THIS IS ESSENTIALLY THE LAYOUT WE TAKE ON FOR THE TABS PER TAB
"""

"""
@app.callback(Output('tabs-content-classes', 'children'),
              Input('tabs-with-classes', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return dbc.Container([
            #html.Div(eeg_inst.create_new_card(['Fp1', "O2"], "fp1 and o2 channels custom card")),
            #dcc.Graph(figure=singlestreamsplot),
            dcc.Graph(figure = eeg_inst.graphStream( "We need to convert this to a draggable, resizable", ['Fp1', "C3", "F3", "O2"])),
            eeg_inst.create_new_card(['Fp1', "C3", "F3","O2", "QuarX"], "other various channels")
            ]
        )
    elif tab == 'tab-2':
        html.Div([
            html.H3('Hopefully this returns a 2d heatmap'),
            # UNCOMMENT BELOW LINE WHEN YOU UNCOMMENT THE ONE BEFORE app.layout = ...
            html.Div(container_2dHeatmap, style={
                     'width': '49%', 'display': 'inline-block'})
        ])
        return #container_2dHeatmap

    elif tab == 'tab-3':
        return html.Div([
            dcc.Graph(figure=theplotiactuallycareabout),
        ])
    elif tab == 'tab-4':
        return html.Div([
            #html.H3('Tab content 4')
        ])



if __name__ == '__main__':
    app.run_server(debug=True)