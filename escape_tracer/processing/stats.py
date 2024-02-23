import numpy as np
from scipy.spatial import distance

def find_escape_stats(speeds, fps, min_escape_frames, max_escape_window):
    
    escape_seq = [0] * min_escape_frames
    escape_frame = len(speeds)

    for i in range(0, len(speeds) - min_escape_frames + 1):
        if list(speeds[i: i+min_escape_frames]) == escape_seq:
            escape_frame = i
            break
    
    escape_time = float(escape_frame)/fps
    max_escape_speed = max(speeds[0:escape_frame])
        
    return escape_time, max_escape_speed

def calculate_speeds(tracking, detected_raw, num_frames, fps, speed_cutoff, exit_roi=None):

    speeds = np.empty(num_frames)
    locs = np.empty((num_frames, 2))
    
    if exit_roi is not None: x1, x2, y1, y2 = exit_roi

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
            
            if exit_roi is not None:
                
                if current_loc is not None:
                    
                    if (x1 < current_loc[0] < x2) and (y1 < current_loc[1] < y2):
                        speed = 0
                        
            recorded_loc = None
        
        if speed > speed_cutoff: 
            speed = speeds[i-1]
                    
        speeds[i] = speed
        locs[i] = recorded_loc
            
    speeds_pps = speeds * fps
    
    return speeds_pps, locs