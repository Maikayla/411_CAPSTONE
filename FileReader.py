from tkinter import filedialog
import pandas as pd
import mne
import pyxdf
import matplotlib.pyplot as plt
class FileReader():
    file_path=""
    file_type=""
    raw_data=""
    raw_df=""
    fname=""

    def __init__(self):
        self.file_path = filedialog.askopenfilename()
        self.file_type = self.file_path[-3:]
        self.fname= self.file_path

    def setRawData(self):
        global raw_data
        if (self.file_type == "bdf"):
           self.raw_data = mne.io.read_raw_bdf(self.file_path)

        elif (self.file_type== "xdf"):
            self.raw_data = pyxdf.load_xdf(self.file_path)
            
    def setDataFrame(self):
        global raw_df
        if (self.file_type=="bdf"):
            self.raw_df = self.raw_data.to_data_frame(index = 'time')

        elif (self.file_type=="xdf"):
            streams, header = pyxdf.load_xdf(self.file_path)

            scale = dict(mag=1e-12, grad=4e-11, eeg=500, eog=150e-6, ecg=5e-4, emg=1e-3, ref_meg=1e-12, misc=1e-3, stim=1, resp=1, chpi=1e-4, whitened=1e2)

            ch_names = []
            for item in streams[2]["info"]["desc"][0]['channels'][0]['channel']:
                ch_names.append(item["label"][0])
    
            ch_types = ["eeg"] * len(ch_names)
            sfreq = int(float(streams[2]["info"]["nominal_srate"][0]))

            data = streams[2]["time_series"].T

            sfreq = float(streams[0]["info"]["nominal_srate"][0])
            info = mne.create_info(ch_names = ch_names, ch_types=ch_types, sfreq = sfreq)
            print(info)
            raw = mne.io.RawArray(data,info,sfreq)
            self.raw_df= raw.to_data_frame()
            raw.plot(scalings=scale)
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