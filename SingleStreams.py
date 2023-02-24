# %% IMPORTS
from sys import displayhook
import mne
import plotly as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# %% SINGLE STREAMS CLASS
class SingleStreams():
    
    ''' initializes SingleStream object's raw_data and raw_df '''
    def __init__(self, file_path):
        self.raw_data = mne.io.read_raw_bdf(file_path)
        self.raw_df = self.raw_data.to_data_frame(index = 'time')
    #

    '''graphs specified streams via multiple subplots'''
    def graphSingleStreams(self, title, streams):
        #  create fig with subplots for each given channel and shared x-axes since all activity occurs over the same span of time
        fig = make_subplots(rows = len(streams), cols = 1, shared_xaxes = True, vertical_spacing = 0.02)

        # loop through each specified channel and plot
        for i in range(len(streams)):
            fig.add_trace(go.Scatter(x = self.raw_df.index, y = self.raw_df.loc[:, streams[i]], mode = 'lines', name = streams[i]), row = i + 1, col = 1)
        #

        fig.update_yaxes(visible = False) # hide y-axes labels for better readability
        fig.update_layout(autosize = False, width = 1400, height = 700, title_text = title, dragmode = "pan") # sets size and given title

        plt.offline.plot(fig, filename = f'OUTPUT/{title}.html')

        return
    #

    '''graphs specified streams on one plot'''
    def graphSingleStreams_Other(self, title, streams):
        fig = go.Figure() # create fig

        # loop through each specified channel and plot
        for i in range(len(streams)):
            fig.add_trace(go.Scatter(x = self.raw_df.index, y = self.raw_df.loc[:, streams[i]], mode = 'lines', name = streams[i]))
        #

        fig.update_yaxes(visible = False) # hide y-axes labels for better readability
        fig.update_layout(autosize = False, width = 1400, height = 700, title_text = title, dragmode = "pan") # sets size and given title
        
        plt.offline.plot(fig, filename = f'OUTPUT/{title}.html') 

        return
    #

# class SingleStreams

# %% WORKING
# create object for sample data
sample_data = SingleStreams('INPUT/semi-dry-demo_signals.bdf')

#display dataframe
displayhook(sample_data.raw_df)

#graph raw_data with specific title and channels
sample_data.graphSingleStreams("All Channels from EEG Data", sample_data.raw_df.columns[:])
sample_data.graphSingleStreams("Specific Channels from EEG Data", ['Fp1', 'Fp2', 'F3'])
sample_data.graphSingleStreams_Other("Simple Plot from EEG Data", ['Fp1', 'Fp2', 'F3', 'Fz', 'Cz', 'Pz'])

# for reference >>> mne.viz.plot_raw(sample_data.raw_data)

# %% REFERENCES
'''
https://plotly.com/python/line-charts/?_ga=2.192353962.1634886175.1672604395-201147630.1672023272
https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.from_dict.html
https://stackoverflow.com/questions/73507706/how-can-i-convert-a-mne-info-into-a-pandas-dataframe
https://plotly.com/python/subplots/
https://community.plotly.com/t/sparklines-from-dataframe/38174/2
https://plotly.com/python/setting-graph-size/
https://community.plotly.com/t/proper-way-to-save-a-plot-to-html/7063/4
'''