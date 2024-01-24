import numpy as np
import pandas as pd
import cv2
from rich.progress import track

from ..utils.utils import *
from ..processing import display
from ..utils import logging

class SignalReader():
    def __init__(self, signal_file, dim, fps, threshold, start_skip, end_skip, brightness_threshold=128):
        
        self.signal_file = signal_file
        self.signal_video = cv2.VideoCapture(self.signal_file)
        self.dim = dim
        self.fps = fps
        self.threshold = threshold
        self.start_skip = start_skip
        self.end_skip = end_skip
        
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
        end_frame = s.size - self.end_skip
        s[:self.start_skip] = 0
        s[end_frame:] = 0
        self.sound = (s > self.threshold).astype(np.int_)
        
    def save(self, save_figure=True):
        
        base_name = self.signal_file.removesuffix('_signal.avi')
        sound_name = base_name + '_sound.csv'
        self.sound.to_csv(sound_name, index=False, header=False)
        
        if save_figure: display.save_sound_plot(self.signal_fig, self.signal_file)
        
    def show_signal_thresholding(self):
        
        self.signal_fig = display.sound_plot(self.time_seconds,
                           self.n_highs, 
                           self.sound, 
                           self.threshold)
        
    def threshold_with_user_confirmation(self):
        
        while True:
            
            self.threshold_signal()
        
            self.show_signal_thresholding()
            
            is_signal_okay = logging.ask_signal_confirmation()

            if is_signal_okay is True:
                break
            
            self.threshold, self.start_skip, self.end_skip = logging.new_signal_attributes(self.threshold, self.start_skip, self.end_skip)
        
            display.close_current_plot()
        
        
        
        
        

 
            

