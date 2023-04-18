from tkinter import filedialog
import pandas as pd
import mne
import pyxdf
import matplotlib.pyplot as plt


import StreamProcessing as sp


class FileReader():
    file_path=""
    file_type=""
    raw_data=""
    raw_df=""
    fname=""
    marker_stream = "" 
    markers_codes = ""
    info = ""
    def __init__(self):
        self.file_path = filedialog.askopenfilename()
        self.file_type = self.file_path[-3:]
        self.fname= self.file_path

    def setRawData(self):
        
        if (self.file_type == "bdf"):
           self.raw_data = mne.io.read_raw_bdf(self.file_path)

        elif (self.file_type== "xdf"):
            (self.raw_data, self.marker_stream, self.markers_codes, self.info, self.raw_df) = sp.read_xdf_retDF(self.file_path)
            
    def setDataFrame(self):
        global raw_df
        if (self.file_type=="bdf"):
            self.raw_df = self.raw_data.to_data_frame(index = 'time')
        elif (self.file_type == "csv"):
            self.raw_df = pd.read_csv(self.file_path)
        plt.show()


if __name__ == "__main__":
    print('Testing file reader.py directly\n')
    file_reader = FileReader()
    file_reader.setRawData()
    file_reader.setDataFrame()
else:
    print('filereader called by : ', __name__)
#https://learn.microsoft.com/en-us/machine-learning-server/python-reference/revoscalepy/rx-read-xdf