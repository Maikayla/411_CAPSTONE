# %% IMPORTS
import FileReader

import mne
import plotly
from plotly.subplots import make_subplots
from dash import dcc
import mpld3
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import os
from typing import Tuple, Callable, Union, List
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import pandas as pd
from IPython.display import clear_output

# %% DATA VISUALIZATION CLASS


class DataVisualization():
    def __init__(self, raw_data, raw_df, marker_stream, markers_codes, info ):
        self.raw_data = raw_data
        self.raw_df = raw_df
        self.times = raw_data.times
        self.marker_stream = marker_stream
        self.markers_codes = markers_codes
        self.info = info

    #
    
    @staticmethod
    def return_offline(fig, title):
        plotly.offline.plot(fig, filename=f'OUTPUT/{title}.html')
    #
    @staticmethod
    def cardcount(op = 0):
        #op should either be -1 or 1, 0 to return current count
        cardcount = 0
        while True: 
            cardcount = cardcount + op
            yield cardcount
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

    def graphStream(self, title, streams, start = None, stop = None):
        ''' graphs specified streams on one plot
        
            Args :
                title : str
                    title for graph
                streams : list(str) or listlike
                    list of strings containing channel names to graph from self.raw_df
                times   : tuple(start : float, stop : float)
                    Start and stop boundaries for plotting (i.e. if we have a sliced sample)
        '''

        
        thisdf = self.raw_df[streams].copy()
        thisdf = thisdf.reset_index().melt(id_vars = 'index', var_name = 'channel', value_name = 'value')
        

        fig = px.line(thisdf, x = 'index', y = 'value', title = title, facet_row = 'channel', facet_row_spacing = 0.0)
        fig.update_yaxes(matches=None,showticklabels=True)
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))

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


    def create_new_card(self, channel_list, title, start = None, stop = None):
        return (html.Div( 
            dbc.Card([
                dbc.CardHeader(title),
                dbc.CardBody(dcc.Graph(figure = self.graphStream(title,channel_list)))
            ])
            )
            )
        


def main():
    pass


# %%
if __name__ == '__main__':
    print('Executing DataVisualization Directly. ')

    main()
else:
    print('DataVisualizations file imported')

# class DataVisualization