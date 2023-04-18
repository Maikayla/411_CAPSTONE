## This program contains a function for reading in xdf data
## It uses the data to filter/process the raw data to find epochs
##      "The reason why we epoch data is to have discrete time periods during which we know 
##      that X was happening on the screen and therefore we suspect that Y cognitive process
##      may be reflected in the data, and as such we want to narrow our analyses to this time
##      period of each trial (and possibly compile across the trials)."
#       https://wiki.uiowa.edu/display/hwanglab/EEG+Preprocessing


import re
import os.path as op
import pyxdf
import mne
import pandas as pd
import numpy as np
import configure as cfg
import sys

##function for reading in the xdf data -- returns raw eeg data
def read_xdf(fpath):
    streams, header = pyxdf.load_xdf(fpath)
    
    for i in range(len(streams)):
        if    streams[i]['info']['name'][0] == 'PRST':              indxStrm_Mrkr   = i
        elif  streams[i]['info']['name'][0] == 'EEG - Impedances':  indxStrm_Imp    = i
        elif  streams[i]['info']['name'][0] == 'EEG':               indxStr_EEG     = i        
        elif  streams[i]['info']['name'][0] == 'Keyboard Events':   indxStr_KeyMrkr = i
        else: print("XDF file format has changed!"); sys.exit(-1)
    #
    
    #EEG Stream
    shapeStream  = [int(float(streams[indxStr_EEG]['footer']['info']['sample_count'][0])), int(streams[indxStr_EEG]['info']['channel_count'][0])] #[sample_count, channel_count]
    chNames      = [x["label"][0] for x in streams[indxStr_EEG]["info"]["desc"][0]['channels'][0]['channel']]
    RawStream_df = pd.DataFrame(data=np.empty(shape=shapeStream), index=None, columns=chNames, dtype=None, copy=None)
    
    for indx, chName in enumerate(chNames):
        RawStream_df[chName] = streams[indxStr_EEG]["time_series"].T[indx]    
    #
    
    RawStream_df[chNames[0:cfg.MBT_NumEEGCh]] = RawStream_df[chNames[0:cfg.MBT_NumEEGCh]] * cfg.uV_2_V
    
    #Create MNE Raw Object
    sfreq_eeg = int(float(streams[indxStr_EEG]["info"]["nominal_srate"][0]))
    sfreq_imp = int(float(streams[indxStrm_Imp]["info"]["nominal_srate"][0]))
    
    ch_types = ["eeg"] * len(chNames)
    info = mne.create_info(ch_names = chNames, ch_types=ch_types, sfreq = sfreq_eeg)
    
    raw_mne = mne.io.RawArray(RawStream_df.T, info, copy= "data")
    
    #Marker Stream
    marker_stream = streams[indxStrm_Mrkr]["time_stamps"]
    marker_stream = marker_stream - streams[indxStr_EEG]["time_stamps"][0]  # To calculate the nth sample. We need the time starting from the beginning of session(since the rocord button was pressed)

    marker_strm_codes = streams[indxStrm_Mrkr]["time_series"]
    markers_codes     = [re.search('<ecode>(.*)</ecode>', marker_strm_codes[i][0] )[1] for i in range(len(marker_strm_codes))]

    return raw_mne, marker_stream, markers_codes, info



##function for reading in the xdf data -- returns raw eeg data
## EDITED FROM ABOVE TO RETURN ALSO DATAFRAME 
## This is to reduce development time. We will need to implement a true workaround later.
def read_xdf_retDF(fpath):
    """
    Edited version of above read_xdf function. Will also return dataframe of timeseries.

    Args:
        fpath : Str or pathlike
            Path to XDF File to be read into

    Returns: 
        raw_mne : mne.io.Raw 
            Mne raw array containing data
            
        marker_stream :
        
        markers_codes :  
        
        info : 

        TODO: Delete below messy notes.

        streams : list[dict] (one dict for each stream)
        Dicts have the following content:
        'time_series': Contains the time series as a [#Channels x #Samples] array of the type declared in ['info']['channel_format'].
        'time_stamps': Contains the time stamps for each sample (synced across streams).
        'info': Contains the meta-data of the stream (all values are strings).
        'name': Name of the stream.
        'type': Content type of the stream ('EEG', 'Events', ...).
        'channel_format': Value format ('int8', 'int16', 'int32', 'int64', 'float32', 'double64', 'string').
        'nominal_srate': Nominal sampling rate of the stream (as declared by the device); zero for streams with irregular sampling rate.
        'effective_srate': Effective (measured) sampling rate of the stream if regular (otherwise omitted).
        'desc': Dict with any domain-specific meta-data.
        fileheader : Dict with file header contents in the 'info' field.
    """
    streams, header = pyxdf.load_xdf(fpath)
    
    for i in range(len(streams)):
        if    streams[i]['info']['name'][0] == 'PRST':              indxStrm_Mrkr   = i
        elif  streams[i]['info']['name'][0] == 'EEG - Impedances':  indxStrm_Imp    = i
        elif  streams[i]['info']['name'][0] == 'EEG':               indxStr_EEG     = i        
        elif  streams[i]['info']['name'][0] == 'Keyboard Events':   indxStr_KeyMrkr = i
        else: print("XDF file format has changed!"); sys.exit(-1)
    #
    
    #EEG Stream
    shapeStream  = [int(float(streams[indxStr_EEG]['footer']['info']['sample_count'][0])), int(streams[indxStr_EEG]['info']['channel_count'][0])] #[sample_count, channel_count]
    chNames      = [x["label"][0] for x in streams[indxStr_EEG]["info"]["desc"][0]['channels'][0]['channel']]
    RawStream_df = pd.DataFrame(data=np.empty(shape=shapeStream), index=None, columns=chNames, dtype=None, copy=None)
    
    for indx, chName in enumerate(chNames):
        RawStream_df[chName] = streams[indxStr_EEG]["time_series"].T[indx]    
    #
    
    RawStream_df[chNames[0:cfg.MBT_NumEEGCh]] = RawStream_df[chNames[0:cfg.MBT_NumEEGCh]] * cfg.uV_2_V
    
    #Create MNE Raw Object
    sfreq_eeg = int(float(streams[indxStr_EEG]["info"]["nominal_srate"][0]))
    sfreq_imp = int(float(streams[indxStrm_Imp]["info"]["nominal_srate"][0]))
    
    ch_types = ["eeg"] * len(chNames)
    info = mne.create_info(ch_names = chNames, ch_types=ch_types, sfreq = sfreq_eeg)
    
    raw_mne = mne.io.RawArray(RawStream_df.T, info, copy= "data")
    
    #Marker Stream
    marker_stream = streams[indxStrm_Mrkr]["time_stamps"]
    marker_stream = marker_stream - streams[indxStr_EEG]["time_stamps"][0]  # To calculate the nth sample. We need the time starting from the beginning of session(since the rocord button was pressed)

    marker_strm_codes = streams[indxStrm_Mrkr]["time_series"]
    markers_codes     = [re.search('<ecode>(.*)</ecode>', marker_strm_codes[i][0] )[1] for i in range(len(marker_strm_codes))]
    print(RawStream_df)
    return raw_mne, marker_stream, markers_codes, info, RawStream_df


"""
##read raw data from xdf
fpath  = "C:/Users/maika/411_misc/2_0_0_Baseline.xdf"
raw, marker_stream, marker_codes,info = read_xdf(fpath)

#round marker time stamps to nearest int
marker_stream_i = (np.rint(marker_stream)).astype(int)
marker_stream_int = np.array(marker_stream_i)


EVENTS = mne.events_from_annotations()


##create the event array -- must be shape(N,3)
column2 = np.zeros(marker_stream_int.shape)
    ## Note: "The second column contains the signal value of the immediately preceding sample, 
    #  and reflects the fact that event arrays sometimes originate from analog voltage channels 
    # (“trigger channels” or “stim channels”). In most cases, the second column is all zeros 
    # and can be ignored.
column3 = np.arange(1,21)
col2 = np.array(column2)
col3 = np.array(column3)

event = np.column_stack((marker_stream_int,col2,col3))
eventArray = event.astype(int)
#print(type(eventArray))

##filter settings
low_cut = 0.1
hi_cut  = 50

##bandpass filter the raw data between .1-50 hz
raw_filt = raw.copy().filter(low_cut, hi_cut)

##plot unfiltered raw data
#raw.plot(start=15, duration=5)

##plot filtered raw data
#raw_filt.plot(start=15, duration=5)

##define epochs
cue_epochs = mne.Epochs( raw=raw_filt, events=eventArray, tmin= -0.8, tmax=1.0, baseline=(None,-0.3))
"""

