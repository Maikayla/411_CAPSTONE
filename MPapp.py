from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

#######################################
"""
    NOTES 
filereader.py should be in the same folder as this file.
As should DataVisualization.py

you will need to pip install mne, plotly, dash_bootstrap_components, pandas, IPython.display

import DataVisualization

filereader = FileReader.FileReader()
filereader.setRawData()
filereader.setDataFrame()

#if testing semi-dry-demo-signals.bdf uncomment the below
###
#filereader.raw_data.rename_channels({'M1':'TP9'})
#filereader.raw_data.rename_channels({'M2':'TP9'})
#filereader.raw_data.drop_channels('Status')
#filereader.raw_data.set_montage(mne.channels.make_standard_montage('easycap-M1'))
###

raw_ = DataVisualization.DataVisualization(filereader.raw_data, filereader.raw_df)

###



"""

#######################################
app = Dash(__name__)
# UNCOMMENT BELOW LINE WHEN YOU RESOLVE THE NOTES ABOVE
# container_2dHeatmap = raw.get_2dHeatmap_child(app)
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

        # Tabbed Menu
        dcc.Tabs(
            id="tabs-with-classes",
            value='tab-1',
            parent_className='custom-tabs',
            className='custom-tabs-container',
            children=[

                dcc.Tab(
                    label='Tab One',
                    value='tab-1',
                    className='custom-tab',
                    selected_className='custom-tab--selected'
                ),
                dcc.Tab(
                    label='Tab Two',
                    value='tab-2',
                    className='custom-tab',
                    selected_className='custom-tab--selected'
                ),
                dcc.Tab(
                    label='Tab Three',
                    value='tab-3', className='custom-tab',
                    selected_className='custom-tab--selected'
                ),
                dcc.Tab(
                    label='Tab Four',
                    value='tab-4',
                    className='custom-tab',
                    selected_className='custom-tab--selected'
                ),
            ]),
        html.Div(id='tabs-content-classes')
    ])


@app.callback(Output('tabs-content-classes', 'children'),
              Input('tabs-with-classes', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Tab content 1')
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2'),
            html.H3('Hopefully this returns a 2d heatmap'),
            # UNCOMMENT BELOW LINE WHEN YOU UNCOMMENT THE ONE BEFORE app.layout = ...
            # html.Div(container_2dHeatmap, style = {'width':'49%','display':'inline-block'})
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H3('Tab content 3')
        ])
    elif tab == 'tab-4':
        return html.Div([
            html.H3('Tab content 4')
        ])


if __name__ == '__main__':
    app.run_server(debug=True)
