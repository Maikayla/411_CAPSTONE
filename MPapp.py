from dash import Dash, html, dcc
import dash
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

#######################################

import FileReader
import DataVisualization
import mne
import mpld3

filereader = FileReader.FileReader()
filereader.setRawData()
filereader.setDataFrame()

filereader.raw_data.rename_channels({'M1': 'TP9'})
filereader.raw_data.rename_channels({'M2': 'TP10'})
filereader.raw_data.drop_channels('Status')
filereader.raw_data.set_montage(
    mne.channels.make_standard_montage('easycap-M1'))

raw_ = DataVisualization.DataVisualization(
    filereader.raw_data, filereader.raw_df)

#######################################

app = Dash(__name__, use_pages=True)

container_2dHeatmap = raw_.get_2dHeatmap_child(app)
singlestreamsplot = raw_.graphSingleStreams(
    'Title of My Single Streams\n Plotly Graph Object', raw_.raw_df.columns[0:5])
othersinglestreamsplot = raw_.graphSingleStreams(
    'Another Single Streams Plot', raw_.raw_df.columns[:])

#######################################

app.layout = html.Div(
    className='bar',
    children=[

        # Header
        html.H1(
            className='header',
            children='MindPrint',
        ),

        # SubHeader
        html.Div(
            className='subHeader',
            children='''Exploring the uniqueness of individuals' brains.''',
        ),

        # NavBar
        html.Div([
            html.Div(
                 dcc.Link(
                     f"{page['name']} - {page['path']}", href=page["relative_path"]
                 )
                 )
            for page in dash.page_registry.values()
        ]),

        dash.page_container
    ])


@app.callback(Output('tabs-content-classes', 'children'),
              Input('tabs-with-classes', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Tab content 1'),
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
            html.H3('Tab content 3'),
            dcc.Graph(figure=othersinglestreamsplot),
        ])
    elif tab == 'tab-4':
        return html.Div([
            html.H3('Tab content 4')
        ])

#######################################


if __name__ == '__main__':
    app.run_server(debug=True)
