# %% IMPORTS
import FileReader

import mne
import plotly
from plotly.subplots import make_subplots

import mpld3
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import os
from typing import Tuple, Callable, Union, List

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import pandas as pd
from IPython.display import clear_output

# %% DATA VISUALIZATION CLASS


class DataVisualization():
    def __init__(self, raw_data, raw_df):
        self.raw_data = raw_data
        self.raw_df = raw_df
        self.times = self.raw_data.times
    #

    @staticmethod
    def return_offline(fig, title):
        plotly.offline.plot(fig, filename=f'OUTPUT/{title}.html')
    #

    def graphSingleStreams(self, title, streams):
        '''graphs specified streams via multiple subplots'''

        #  create fig with subplots for each given channel and shared x-axes since all activity occurs over the same span of time
        fig = make_subplots(rows=len(streams), cols=1,
                            shared_xaxes=True, vertical_spacing=0.02)

        # loop through each specified channel and plot
        for i in range(len(streams)):
            fig.add_trace(go.Scatter(
                x=self.raw_df.index, y=self.raw_df.loc[:, streams[i]], mode='lines', name=streams[i]), row=i + 1, col=1)
        #

        # hide y-axes labels for better readability
        fig.update_yaxes(visible=False)
        fig.update_layout(autosize=False, width=1400, height=700,
                          title_text=title, dragmode="pan")  # sets size and given title

        """ plotly. offline. plot(fig, filename=f'OUTPUT/{title}.html')"""

        return fig
    #

    def graphSingleStreams_Other(self, title, streams):
        '''graphs specified streams on one plot'''
        fig = go.Figure()  # create fig

        # loop through each specified channel and plot
        for i in range(len(streams)):
            fig.add_trace(go.Scatter(
                x=self.raw_df.index, y=self.raw_df.loc[:, streams[i]], mode='lines', name=streams[i]))
        #

        # hide y-axes labels for better readability
        fig.update_yaxes(visible=False)
        fig.update_layout(autosize=False, width=1400, height=700,
                          title_text=title, dragmode="pan")  # sets size and given title

        return fig

    def get_2dHeatmap_child(self, app):
        """
        When passed a dash app instance as an argument, this method will return
        a dash bootstrap components (dbc) container. The container will hold
        a 2d heatmap element from the class instance Raw|Evoked|Epoched data and make it navigable.

        This one isn't returned as a plotly Graph Object (i.e. plotly.go)
        The reason is because the contour artist for 2d heatmaps and contour drawings doesn't easily transfer.
        Furthermore, we rely on the MNE library when possible for accuracy.
        Since this is using a builtin for MNE we don't have to worry about testing the heatmap function for accuracy.

        ARGUMENTS
            app :: Dash instance
                This method was written so this class can be imported and used modularly for another dash app.
        RETURNS
            html_heatmap :: dbc.Container
                DBC container holding a div with 2d heatmap/contour plot for the mne instance associated with the call.
                The div also has a slider for navigation along the time axis.

            _ :: str
                string output stating 2d heatmap selected at n seconds.

        TODO: slice time slots.
              remove noVar output.


        """
        self.start = 0
        self.stop = len(self.raw_data.times)-1
        self.sample_freq = self.raw_data.info['sfreq']
        self.HeatmapContainerElement = dbc.Container([
            html.Iframe(
                id='2DHeatmaps',
                srcDoc=None,
                style={'border-width': '3', 'width': '100%', 'height': '550px'}
                ),
            dcc.Slider(
                self.times[self.start],
                self.times[self.stop-1],
                self.times[1]-self.times[0],
                id="Time-update-slider",
                value=self.start,
                marks=None,
                updatemode='drag'
                ),
            html.Div(id='update-slider-timeinfo',
                        style={'width': '100%', 'height': '25%'})
            ])
        # end layout

        @app.callback(
            Output(component_id='2DHeatmaps', component_property='srcDoc'),
            Output('update-slider-timeinfo', 'children'),
            Input(component_id='Time-update-slider', component_property='value'))
        def _plot_2dheatmap(selected_time):
            fig, ax = plt.subplots()
            self.unraveled_eegs = np.ravel(
                self.raw_data.get_data(
                    start=int(selected_time/(1/self.sample_freq)),
                    stop=int(selected_time/(1/self.sample_freq))+1
                )
            )
            mne.viz.plot_topomap(self.unraveled_eegs,
                                self.raw_data.info, axes=ax, show=False)

            html_heatmap = mpld3.fig_to_html(fig)

            # mpld3.show(html_heatmap)

            return html_heatmap, f'2D Heatmap at {selected_time} seconds'

        return self.HeatmapContainerElement


def main():
    filereader = FileReader.FileReader()
    filereader.setRawData()
    filereader.setDataFrame()

    # To be used when testing the semi-dry-demo-signals bdf file.
    ##
    #
    filereader.raw_data.rename_channels({'M1': 'TP9'})
    filereader.raw_data.rename_channels({'M2': 'TP10'})
    filereader.raw_data.drop_channels('Status')
    filereader.raw_data.set_montage(
        mne.channels.make_standard_montage('easycap-M1'))
    #
    ##
    ###
    ####

    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    print(filereader.raw_data.info)

    raw_ = DataVisualization(filereader.raw_data, filereader.raw_df)

    container_2dHeatmap = raw_.get_2dHeatmap_child(app)

    app.layout = html.Div(
        [
            html.Div(
                [
                    html.H1('Testing out DataVisualization.py'),
                    html.H2('Text above container'),
                    html.Div(
                        container_2dHeatmap,
                        style={'width': '49%', 'height': '45%',
                               'display': 'inline-block'}
                    ),
                    html.Div(
                        html.H2('Text to the right of the container'),
                        style={'width': '49%', 'display': 'inline-block'}
                    ),
                    html.Div(
                        [
                            html.H2('Above: Callable & Containerized 2D Heatmap')
                        ]
                    )
                ], style={'height': '800px'}),
            html.Div(
                [
                    html.H1('Outermost, lowermost Div Element'),

                ], style={})
        ])

    app.run_server(debug=True)


# %%
if __name__ == '__main__':
    print('Executing DataVisualization Directly. ')

    main()
else:
    print('DataVisualizations file imported')

# class DataVisualization
