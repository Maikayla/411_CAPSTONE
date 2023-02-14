#version : "#.#.##"   

"""
Description:
    Reading from XDF file & displaying the streams

Authors:
    Dr. Omer Muhammet Soysal
    Muhammed Zahid Yeter

Doc:
    https://anaconda.org/conda-forge/pyxdf
    https://github.com/xdf-modules/pyxdf/blob/main/pyxdf/pyxdf.py
    https://mne.tools/dev/generated/mne.io.Raw.html#mne.io.Raw.plot
"""

# IMPORTS
#custom imports
import config            as cfg
import signal_processing as sp

#other imports
import math
from   matplotlib import pyplot as plt
import mne
import numpy  as np
import pandas as pd 
import pyxdf
import os
import time

#%% SETTINGS
#print("get_backend: ",rcParams['backend'])
#use('Qt5Agg')
mne.viz.set_browser_backend("matplotlib", verbose=False)

#%% USER INPUT (!!!    WARNING: may override config.py   !!!)
#Stimulus and subject
stimulusID  = 'mu_01' #{cg_me; mo_eb, mo_hd, mo_hn, mo_fe; mu_01,mu_02,mu_03; mw_01, mw_02, mw_03; sq_00; ms_01; wg_00}
subject     = 1
sessionLst  = [1] 

#path
pathRootIn  = os.getcwd()+"/INPUT/MPMB/TEST/prtcl_2"
pathRootOut = os.getcwd()+"/OUTPUT/MPMB/TEST"
imageName   = ""

#filtering
use_filtered_data = True
filterType        = '2'   #0: Only Notch, 1: Only the other filter, 2: Both Notch and the other
freqsImpedance    = 125    #To stop-pass impedance current signal with 125 Hz
freqsNotch        = [60,120,180,240]    #[60,120,180,240,300,360,420,480] <TODO: Make this generic based on sample frequency>
freqsOther        = [1, None]     #No filtering: [0.00001, None]; stop-band for main-line 1st harmonic: [62, 58]


#Display
remove_dc = True
duration=float('inf') #shapeStream[0]/cfg.sampleFreq

#Save
save_figures = False
save_files   = False

#Plot
plot_raw      = dict( main = True, Hz_1_4  = True, Hz_4_8 = True, Hz_8_13 = True, Hz_13_32 = True, Hz_32_120 = True, Hz_over_120 = True)
plot_spectrum = dict( main = True)
plot_filtered = dict( main = True)

#%% BODY
#Create sub folder for pathRootOut
if not os.path.exists(pathRootOut):
    os.makedirs(pathRootOut)
    print(pathRootOut, " created.")
#

#Create sub folder for the subject
pathSub = pathRootOut+"/s"+str(subject)
if not os.path.exists(pathSub):
    os.mkdir(pathSub)
    print(pathSub, " created.")
#

#Create sub folders for sessions
for session in sessionLst:
    pathSub = pathRootOut+"/s"+str(subject)+"/s"+str(session)
    if not os.path.exists(pathSub):
        os.mkdir(pathSub)
        print(pathSub, " created.")
    #
#

#Create sub folder for the stimulus
pathSub = pathRootOut+"/s"+str(subject)+"/s"+str(session)+"/"+stimulusID
if not os.path.exists(pathSub):
    os.mkdir(pathSub)
    print(pathSub, " created.")
#

#Read configuration values
chNameEEG    = cfg.chNameEEG
chNameMotion = cfg.chNameMotion
chNameRegion = cfg.chNameRegion

for session in sessionLst:
    #Reading the Data
    dataFile = pathRootIn + f"/s{subject}/s{session}/s{subject}_s{session}_{stimulusID}.xdf"

    #XDF Reader
    streams, header = pyxdf.load_xdf(dataFile)      #streams: List: [disct-1 for impedance, disct-2 for EEG and motion streams, disct-3 for key markers]

    #ToDo: Instead of "streams[indxStr_EEG]", it can be replaced with "streamEEG"
    for i in range(len(streams)):
        if    streams[i]['info']['type'][0][0:3] == 'Mar': indxStrm_Mrkr = i
        elif  streams[i]['info']['type'][0][0:3] == 'Imp': indxStrm_Imp  = i
        elif  streams[i]['info']['type'][0][0:3] == 'EEG': indxStr_EEG   = i
        else: print("It XDF file format has changed!"); _sysExit(-1)
    #

    shapeStream = [int(float(streams[indxStr_EEG]['footer']['info']['sample_count'][0])), int(streams[indxStr_EEG]['info']['channel_count'][0])] #[sample_count, channel_count]
    chNamesXdf = [x["label"][0] for x in streams[indxStr_EEG]["info"]["desc"][0]['channels'][0]['channel']]
    dataStreams = pd.DataFrame(data=np.empty(shape=shapeStream), index=None, columns=chNamesXdf, dtype=None, copy=None)

    indx = 0
    for indx,chName in enumerate(chNamesXdf):
        dataStreams[chName] = streams[indxStr_EEG]["time_series"].T[indx] #shape: [sample_count, channel_count]; ( dataRawCh - np.median(dataRawCh) )
        indx += 1
    #

    for rgn,rgnChNames in chNameRegion.items():
        #ToDO: Check the effect of dividing by cfg.V_2_uV = 10^6
        dataRawEEG  = dataStreams[rgnChNames].T.copy() #shape: [channel_count, sample_count]; add "/ cfg.V_2_uV" for scaling in displaying
        #Rereferencing; remove_dc = True can be used, instead:
        #dataRawEEG = dataRawEEG.subtract(dataRawEEG.median(axis=1),axis=0)

        #sampleFreq = int(float(streams[indxStr_EEG]["info"]["nominal_srate"][0]))    #if need to override config.py
        chTypesEEG  = ["eeg"] * len(rgnChNames)
        cfgInfo = mne.create_info(ch_names = rgnChNames, ch_types = chTypesEEG, sfreq = cfg.sampleFreq)
   
        #%%filtering the data    
        if filterType   == '0':
            data_filtered = sp.eeg_filter(dataRawEEG,True,cfgInfo,freqsNotch)
            data_filtered = sp.eeg_filter(data_filtered,False,cfgInfo,[freqsImpedance+5,freqsImpedance-5])  #remove the component due to impedance recording
        elif filterType == '1':
            data_filtered = sp.eeg_filter(dataRawEEG,False,cfgInfo,freqsOther) # low_freq and high_freq parameters defines the filter Type!!! Refer to function description.
        else:
            data_filtered = sp.eeg_filter(dataRawEEG,True,cfgInfo,freqsNotch)
            data_filtered = sp.eeg_filter(data_filtered,False,cfgInfo,[freqsImpedance+5,freqsImpedance-5])  #remove the component due to impedance recording
            data_filtered = sp.eeg_filter(data_filtered,False,cfgInfo,freqsOther) # low_freq and high_freq parameters defines the filter Type!!! Refer to function description.
        #

        if use_filtered_data:
            data = data_filtered
            rawFiltered = 'Filtered'
        else:
            data = dataRawEEG
            rawFiltered = 'Raw'
        #
        
        #%% Extract Freq bands
        data_freq_bands = sp.freq_bands()
        data_freq_bands.extract_freq_bands(data,cfgInfo)

        #plot raw data.    
        dataRawEEGmne                     = mne.io.RawArray(dataRawEEG.copy(), cfgInfo, verbose = False)
        dataFiltered_EEGmne               = mne.io.RawArray(data_filtered.copy(), cfgInfo, verbose = False)
    
        print(f"MAIN : Plotting main raw data.")
        fig_raw = dataRawEEGmne.plot(clipping=None,
                                     title=f"Raw {rgn} - {imageName}, {subject}, {session} - {stimulusID}",
                                     scalings = cfg.scale_raw,
                                     show = False,
                                     verbose = False,
                                     duration=duration,
                                     n_channels=len(rgnChNames),
                                     remove_dc=remove_dc)
        if plot_raw["main"] == False:
            plt.close(fig_raw)
        #

        print(f"MAIN : Plotting spectrums (raw data).")
        fig_spectrumRaw = dataRawEEGmne.compute_psd().plot()
        fig_spectrumRaw.suptitle(f"Freq Spectrum (raw-{rgn}) - {imageName}, {subject}, {session} - {stimulusID}")
        if plot_spectrum["main"] == False:
            plt.close(fig_spectrumRaw)
        #

        print(f"MAIN : Plotting spectrums (filtered).")
        fig_spectrumFilterd = dataFiltered_EEGmne.compute_psd().plot()
        fig_spectrumFilterd.suptitle(f"Freq Spectrum (filtered-{rgn}) - {imageName}, {subject}, {session} - {stimulusID}")
        if plot_spectrum["main"] == False:
            plt.close(fig_spectrumFilterd)
        #

        print(f"MAIN : Plotting filtered data.")
        #plt.figure()
        fig_data_filtered = dataFiltered_EEGmne.plot(clipping=None,
                                                     title=f"Filtered {rgn} - {imageName}, {subject}, {session} - {stimulusID}",
                                                     scalings = cfg.scale_raw,
                                                     show = False,
                                                     verbose = False,
                                                     duration=duration,
                                                     n_channels=len(rgnChNames),
                                                     remove_dc=remove_dc)
        if plot_filtered["main"] == False:
            plt.close(fig_data_filtered)
        #

        print(f"MAIN : Saving figures")
        if save_figures == True:
            fig_raw.savefig(pathRootOut + f"/s{subject}/s{session}/{stimulusID}/{stimulusID}_raw_{imageName}_s{subject}_s{session}.png")
            fig_spectrumRaw.savefig(pathRootOut + f"/s{subject}/s{session}/{stimulusID}/{stimulusID}_spectrum_{imageName}_s{subject}_s{session}.png")
            fig_data_filtered.savefig(pathRootOut + f"/s{subject}/s{session}/{stimulusID}/{stimulusID}_filtered_{imageName}_s{subject}_s{session}.png")
        #
    
        #%%PLOT BANDS
        #plot bands raw data
        print(f"MAIN : Plotting bands {rawFiltered} data.")
        i = 0
        for itemL in data_freq_bands.mneraw_dict.values():
            fig_raw = itemL.plot(clipping=None,
                                 title = f"{rawFiltered} {rgn} - {cfg.frequency_bands[i]}, {imageName}, {subject}, {session} - {stimulusID}",
                                 scalings = cfg.scale_raw,
                                 show = False,
                                 verbose = False,
                                 duration=duration,
                                 n_channels=len(rgnChNames),
                                 remove_dc=remove_dc)
            
            if plot_raw[cfg.frequency_bands[i]] == False:
                plt.close(fig_raw)
            #
        
            if save_figures == True:
                fig_raw.savefig(pathRootOut + f"/s{subject}/s{session}/{stimulusID}/{stimulusID}_{rawFiltered}_{cfg.frequency_bands[i]}_{imageName}_{subject}_{session}.png")  
            #
            i += 1
        #End for

        #%% Save
        if save_files == True:
            print(f"MAIN : Saving filtered data.") 
            data_filtered.to_csv(pathRootOut + f"/s{subject}/s{session}/{stimulusID}/{stimulusID}_filtered_{imageName}_s{subject}_s{session}.csv")
        
            #save bands raw data.
            print(f"MAIN : Saving bands {rawFiltered} data.")
            i = 0
            for itemL in data_freq_bands.raw_dict.values():
                itemL.T.to_csv(pathRootOut + f"/s{subject}/s{session}/{stimulusID}/{stimulusID}_{rawFiltered}_{imageName}_{cfg.frequency_bands[i]}_s{subject}_s{session}.csv", index = False)
                i += 1
            #
        #End if
        #plt.show() #testing
    #for rgn
#End for
plt.show() #mne.io.RawArray(<some data>, <some info>).plot(block=True)
print("DONE")