import numpy as np
import pandas as pd

def read_stim_file(stim_file, num_frames):
    
    stim_tracking = pd.read_csv(stim_file)
    raw_stim = np.array(stim_tracking.to_numpy().flatten(), dtype=bool)
    
    stim = conform_stim(raw_stim, num_frames)
    
    return stim

def conform_stim(stim, num_frames):
    
    stim_length = stim.size
    disparity = num_frames - stim_length
    
    if disparity > 0:
        conformed_stim = np.append(stim, np.zeros(disparity, dtype=bool))
        
    elif disparity < 0:
        conformed_stim = stim[:disparity]
        
    else:
        conformed_stim = stim
        
    return conformed_stim

def get_stim_events(stim):
    
    stim_int = stim.astype(np.int8) 
    stim_event_frames = []
    
    for index, value in enumerate(stim_int):
        if index == 0:
            prev_value = 0
        else:
            flip = value - prev_value
            if flip == 1:
                stim_event_frames.append(index)
            prev_value = value
            
    return stim_event_frames
