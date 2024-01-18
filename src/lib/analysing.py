import numpy as np
import pandas as pd
from scipy.spatial import distance

from .utils import *
from .settings import settings

def calculate_speeds(tracking, detections, num_frames, fps, base_path, exit_roi=None):

    # calculate speeds
    speed_ppf, locs = get_metrics(tracking, detections, num_frames, exit_roi)
    speed_pps = speed_ppf * fps
    
    speed_tracking = pd.DataFrame((speed_pps, locs))
    speed_tracking.to_csv(base_path + '_speeds.csv')
    
    return speed_pps, locs

def find_escape_stats(speeds, fps):
    
    minmum_escape_frames = settings["minmum_escape_frames"]
    max_escape_window = settings["max_escape_window"]
    
    escape_seq = [0] * minmum_escape_frames
    escape_frame = None

    for i in range(0, len(speeds) - minmum_escape_frames + 1):
        if list(speeds[i: i+minmum_escape_frames]) == escape_seq:
            escape_frame = i
            break
    
    if escape_frame is not None:
        escape_time = float(escape_frame)/fps
        if escape_time < max_escape_window:
            max_escape_speed = max(speeds)
        else:
            escape_time = max_escape_speed = None
    else:
        escape_time = max_escape_speed = None
        
    return escape_time, max_escape_speed

def get_metrics(tracking, detected_raw, num_frames, roi):
    
    speeds = np.empty(num_frames)
    locs = np.empty((num_frames, 2))
    speed_cutoff = settings["speed_cutoff"]
    
    if roi is not None: x1, x2, y1, y2 = roi

    detected = [index for index, frame_detected in enumerate(detected_raw) if frame_detected]
    for i in range(num_frames):

        if i == 0:
            speed = 0
            recorded_loc = current_loc = None
            
        elif i in detected:
            current_loc =  np.concatenate((tracking['x'].values[i].flatten(), 
                                          tracking['y'].values[i].flatten()))
            if i-1 in detected:
                last_loc = np.concatenate((tracking['x'].values[i-1].flatten(), 
                                          tracking['y'].values[i-1].flatten()))
                speed = distance.euclidean(current_loc, last_loc)
                
            recorded_loc = current_loc
             
        else:
            
            if roi is not None:
                
                if current_loc is not None:
                    
                    if (x1 < current_loc[0] < x2) and (y1 < current_loc[1] < y2):
                        speed = 0
                        
            recorded_loc = None
        
        if speed > speed_cutoff: 
            speed = speeds[i-1]
                    
        speeds[i] = speed
        locs[i] = recorded_loc
            
    return speeds, locs