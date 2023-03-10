from dash import Dash, html, dcc
import dash
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

#######################################

import FileReader
import DataVisualization
import mne
import mpld3
filereader = FileReader.FileReader()
filereader.setRawData()

filereader.setDataFrame()

# if testing semi-dry-demo-signals.bdf uncomment the below
###
filereader.raw_data.rename_channels({'M1': 'TP9'})
filereader.raw_data.rename_channels({'M2': 'TP10'})
filereader.raw_data.drop_channels('Status')
filereader.raw_data.set_montage(
    mne.channels.make_standard_montage('easycap-M1'))
###

raw_ = DataVisualization.DataVisualization(
    filereader.raw_data, filereader.raw_df)

###


"""
"""

#######################################
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SLATE, dbc.icons.FONT_AWESOME],)


container_2dHeatmap = raw_.get_2dHeatmap_child(app)
singlestreamsplot = raw_.graphSingleStreams(
    'Title of My Single Streams\n Plotly Graph Object', raw_.raw_df.columns[0:5])
othersinglestreamsplot = raw_.graphSingleStreams(
    'Another Single Streams Plot', raw_.raw_df.columns[:])

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


@app.callback(Output('tabs-content-classes', 'children'),
              Input('tabs-with-classes', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            #html.H3('Tab content 1'),
            dcc.Graph(figure=singlestreamsplot)

        ])
    elif tab == 'tab-2':
        """html.Div([
            html.H3('Tab content 2'),
            html.H3('Hopefully this returns a 2d heatmap'),
            # UNCOMMENT BELOW LINE WHEN YOU UNCOMMENT THE ONE BEFORE app.layout = ...
            html.Div(container_2dHeatmap, style={
                     'width': '49%', 'display': 'inline-block'})
        ])"""
        return container_2dHeatmap

    elif tab == 'tab-3':
        return html.Div([
            #html.H3('Tab content 3'),
            dcc.Graph(figure=othersinglestreamsplot),
        ])
    elif tab == 'tab-4':
        return html.Div([
            #html.H3('Tab content 4')
        ])



if __name__ == '__main__':
    app.run_server(debug=True)
