module_name = "config"
"""
Description: 
    This module includes project confgurations and global variables.

Authors:
    Dr. Omer Muhammet Soysal
    Muhammed Zahid Yeter

Doc:

"""

#%%IMPORTS
import mne
from os import chdir as osChdir

#%% USER INPUT
regionOptionBED = 1     # [1 2]
sampleFreq      = 500   # sampling frequency of the amplifier unit
data_source     = "MBT" # {BED, MBT: mBrain}

#%% CONSTANTS
#Maximal State algorithm parameters.
tR  = 0.1  # Torelarance [0 1]
sTh = 100  # Saturation Threshold uV

#Channels and their neighbourhood definition:
if (data_source == "MBT"):    
    
    chNameEEG             = ['Fp1','Fp2','AFz','F3','Fz','F4',
                            'C3','Cz','C4',
                            'CPz','P3','Pz','P4',
                            'POz','O1','O2',
                            'F7','T7','M1','P7',
                            'F8','T8','M2','P8'] #['Fp1', 'Fp2', 'F3', 'F4', 'C3', 'C4', 'P3', 'P4', 'O1', 'O2', 'F7', 'F8', 'T7', 'T8', 'P7', 'P8', 'Fz', 'Cz', 'Pz', 'M1', 'M2', 'AFz', 'CPz', 'POz'] 
    chNameMotion          = ['AccX','AccY','AccZ',
                             'GyroX','GyroY','GyroZ',
                             'QuarW','QuarX','QuarY','QuarZ']
    ch_types             = ['eeg'] * len(chNameEEG)
    neighbourhood_dict   = dict(Fp1 = ["F7" , "F3" , "AFz"              ],
                                Fp2 = ["F8" , "F4" , "AFz"              ],                                
                                F3  = ["F7" , "Fp1", "AFz", "Fz"        ],                                
                                F4  = ["F8" , "Fp2", "AFz", "Fz"        ],                                
                                C3  = ["T7" , "Cz"                      ],                                
                                C4  = ["T8" , "Cz"                      ],                                
                                P3  = ["P7" , "Pz"                      ],                                
                                P4  = ["P8" , "Pz"                      ],                                
                                O1  = ["POz"                            ],
                                O2  = ["POz"                            ],                                
                                F7  = ["T7" , "Fp1", "F3"               ],
                                F8  = ["T8" , "Fp2", "F4"               ],                                
                                T7  = ["M1" , "F7" , "C3"               ],
                                T8  = ["M2" , "F8" , "C4"               ],                                
                                P7  = ["M1" , "P3"                      ],
                                P8  = ["M2" , "P4"                      ],                                
                                Fz  = ["F3" , "AFz", "F4"               ],                                
                                Cz  = ["C3" , "C4" , "CPz"              ],                                
                                Pz  = ["POz", "P3" , "CPz", "P4"        ],                                
                                M1  = ["T7" , "P7"                      ],
                                M2  = ["T8" , "P8"                      ],                                
                                AFz = ["Fz" , "F3" , "Fp1", "Fp2", "F4" ],                                
                                CPz = ["Pz" , "Cz"                      ],                                
                                POz = ["O1" , "Pz" , "O2"               ])
    
    regions                            = ["frontal", "central",  "temporal_left", "temporal_right", "parietal", "occipital"]
    ch_types_for_regions               = ['eeg'] * len(regions)
    chNameRegion = dict(frontal        = ["Fp1", "Fp2", "AFz", "F3", "Fz", "F4"  ],
			            central        = ["C3" , "Cz" , "C4"                     ],
                        temporal_left  = ["F7" , "T7" , "M1" , "P7"              ],
                        temporal_right = ["F8" , "T8" , "M2" , "P8"              ],
                        parietal       = ["CPz", "P3" , "Pz" , "P4"              ],
                        occipital      = ["POz", "O1" , "O2"                     ]) 
elif data_source == "BED":     
    
    chNameEEG             = ['AF3','F3' ,'F7' ,'FC5','T7' ,'P7' ,'O1' ,'O2' ,'P8' ,'T8' ,'FC6','F8' ,'F4' ,'AF4'] 
    ch_types             = ['eeg'] * len(chNameEEG)
    neighbourhood_dict   = dict(AF3 = ["F3" , "F7"        ],
                                F3  = ["AF3", "FC5"       ],
                                F7  = ["AF3", "FC5"       ],
                                FC5 = ["F3" , "F7" , "T7" ],
                                T7  = ["FC5", "P7"        ],
                                P7  = ["T7" , "O1"        ],
                                O1  = ["P7" , "O2"        ],
                                O2  = ["O1" , "P8"        ],
                                P8  = ["O2" , "T8"        ],
                                T8  = ["P8" , "FC6"       ],
                                FC6 = ["F4" , "T8" , "F8" ],
                                F8  = ["AF4", "FC6"       ],
                                F4  = ["FC6", "AF4"       ],
                                AF4 = ["F4" , "F8"        ])
    
    
    #Region configurations
    if regionOptionBED == 1:
        regions                            = ["frontal_left", "frontal_right", "temporal_left", "temporal_right", "occipital"]
        ch_types_for_regions               = ['eeg','eeg','eeg','eeg','eeg'] # The length of "ch_types_for_regions" must be equal to the length of "regions"
        chNameRegion = dict(frontal_left   = ['AF3','F3' ,'F7' ,'FC5'],
                            frontal_right  = ['FC6','F8' ,'F4' ,'AF4'],
                            temporal_left  = ['T7' ,'P7'             ],
                            temporal_right = ['P8' ,'T8'             ],
                            occipital      = ['O1' ,'O2'             ])
    elif regionOptionBED ==2:
        regions                 = ["frontal_left", "frontal_midLeft", "frontal_right", "frontal_midRight", "temporal_left", "temporal_right", "occipital"]
        ch_types_for_regions    = ['eeg','eeg','eeg','eeg','eeg','eeg','eeg']
        chNameRegion            = dict(frontal_left      = ['F7' ,'FC5'],
    			                       frontal_midLeft   = ['AF3','F3' ],
                                       frontal_right     = ['FC6','F8' ],
                                       frontal_midRight  = ['F4' ,'AF4'],
                                       temporal_left     = ['T7' ,'P7' ],
                                       temporal_right    = ['P8' ,'T8' ],
                                       occipital         = ['O1' ,'O2' ])
#End if "data_source"
frequency_bands      = ["Hz_1_4", "Hz_4_8", "Hz_8_13", "Hz_13_32", "Hz_32_120", "Hz_over_120"]

#%%
scale_diff   = dict(mag=1e-12, grad=4e-11, eeg=15,      eog=150e-6, ecg=5e-4, emg=1e-3, ref_meg=1e-12, misc=1e-3, stim=1, resp=1, chpi=1e-4, whitened=1e2)
scale_raw    = dict(mag=1e-12, grad=4e-11, eeg=5e-4,    eog=150e-6, ecg=5e-4, emg=1e-3, ref_meg=1e-12, misc=1e-3, stim=1, resp=1, chpi=1e-4, whitened=1e2)
scale_states = dict(mag=1e-12, grad=4e-11, eeg=2,       eog=150e-6, ecg=5e-4, emg=1e-3, ref_meg=1e-12, misc=1e-3, stim=1, resp=1, chpi=1e-4, whitened=1e2)
    
#info          = mne.create_info(ch_names = chNameEEG, ch_types=ch_types,             sfreq = sampleFreq)
#info_regional = mne.create_info(ch_names = regions,  ch_types=ch_types_for_regions, sfreq = sampleFreq)

# =============================================================================
# V_2_uV = 1E6
# uV_2_V = 1E-6
# 
# =============================================================================
MBT_NumEEGCh = 24
V_2_uV = 1E6
uV_2_V = 1E-6  

#Signal Processing
outlier_rate = 1.5 

if __name__ == "__main__":
    print("\"config\" module begins.")
#
else:
    print("\"config\" module imported.")
#