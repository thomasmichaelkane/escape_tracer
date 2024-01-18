import os
import numpy as np
import pandas as pd

def read_sound_file(sound_file, num_frames):
    
    folder_name, file_name = os.path.split(sound_file)
    base_name = file_name.removesuffix('_sound.csv')
    sound_tracking = pd.read_csv(sound_file)
    raw_sound = np.array(sound_tracking.to_numpy().flatten(), dtype=bool)
    
    sound = conform_sound(raw_sound, num_frames)
    
    return sound, folder_name, base_name

def conform_sound(sound, num_frames):
    
    sound_length = sound.size
    disparity = num_frames - sound_length
    
    if disparity > 0:
        conformed_sound = np.append(sound, np.zeros(disparity, dtype=bool))
        
    elif disparity < 0:
        conformed_sound = sound[:disparity]
        
    else:
        conformed_sound = sound
        
    return conformed_sound

def get_sound_events(sound):
    
    sound_int = sound.astype(np.int8) 
    sound_event_frames = []
    
    for index, value in enumerate(sound_int):
        if index == 0:
            prev_value = 0
        else:
            flip = value - prev_value
            if flip == 1:
                sound_event_frames.append(index)
            prev_value = value
            
    return sound_event_frames 