import numpy as np
import pandas as pd
import cv2
from rich.progress import track

from escape_tracer.processing import display, stim
from escape_tracer.utils import logging
from escape_tracer.utils.util_functions import *

class SignalReader():
    def __init__(self, signal_file, dim, fps, threshold, start_frame, end_frame, expected_range, brightness_threshold=128):
        
        self.signal_file = signal_file
        self.signal_video = cv2.VideoCapture(self.signal_file)
        self.dim = dim
        self.fps = fps
        self.threshold = threshold
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.expected_range = expected_range
        
        self.n_highs = []
        n_frames = int(self.signal_video.get(cv2.CAP_PROP_FRAME_COUNT))
        
        for _ in track(range(n_frames), description="Analysing signal..."):
            
            ret, color_frame = self.signal_video.read()
            
            if ret:     
                frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2GRAY)
                bin_frame = (frame > brightness_threshold).astype(np.int_)
                
                n_high = bin_frame.sum()
                self.n_highs.append(n_high)
                              
                # # Press Q on keyboard to  exit
                # if cv2.waitKey(0) & 0xFF == ord('q'):
                #     break
                
            else:
                break

        num_points = len(self.n_highs)

        time_frames = np.array(range(0, num_points))
        self.time_seconds = time_frames/self.fps
        
        self.signal_video.release()
        cv2.destroyAllWindows()
        
    def threshold_signal(self):
    
        s = pd.Series(self.n_highs)
        end_frame = s.size - self.end_frame
        s[:self.start_frame] = 0
        s[end_frame:] = 0
        self.stim = (s > self.threshold).astype(np.int_)
        
    def save(self, save_figure=True):
        
        base_name = self.signal_file.removesuffix('_signal.avi')
        stim_name = base_name + '_stim.csv'
        self.stim.to_csv(stim_name, index=False, header=False)
        
        if save_figure: display.save_stim_plot(self.signal_fig, self.signal_file)
        
    def show_signal_thresholding(self):
        
        self.signal_fig = display.stim_plot(self.time_seconds,
                           self.n_highs, 
                           self.stim, 
                           self.threshold)
        
    def threshold_with_user_confirmation(self):
        
        while True:
            
            self.threshold_signal()
        
            self.show_signal_thresholding()
            
            is_signal_okay = logging.ask_signal_confirmation()

            if is_signal_okay is True:
                break
            
            self.threshold, self.start_frame, self.end_frame = logging.new_signal_attributes(self.threshold, self.start_frame, self.end_frame)
        
            display.close_current_plot()
        
        
        
        
        

 
            

