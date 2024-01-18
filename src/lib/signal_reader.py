import numpy as np
import pandas as pd
import cv2
from rich import track

from .utils import *
from . import display

class SignalReader():
    def __init__(self, signal_file, dim, fps):
        
        self.signal_file = signal_file
        self.signal_video = cv2.VideoCapture(self.signal_file)
        self.dim = dim
        self.fps = fps
        
    def read(self):

        self.averages = self.n_highs = []
        n_frames = int(self.signal_video.get(cv2.CAP_PROP_FRAME_COUNT))
        
        for _ in track(range(n_frames), description="Analysing signal..."):
            
            ret, color_frame = self.signal_video.read()
            
            if ret:     
                frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2GRAY)
                bin_frame = (frame > 100).astype(np.int_)
                
                n_high = bin_frame.sum()
                self.n_highs.append(n_high)
                
                average = np.average(frame)
                self.averages.append(average)
                
                # Press Q on keyboard to  exit
                if cv2.waitKey(0) & 0xFF == ord('q'):
                    break
                
            else:
                break

        num_points = len(self.averages)

        time_frames = np.array(range(0, num_points))
        self.time_seconds = time_frames/self.fps
        
        self.signal_video.release()
        cv2.destroyAllWindows()
        
    def threshold_signal(self, threshold, start_skip=0, end_skip=0):
    
        self.threshold = threshold
        s = pd.Series(self.n_highs)
        end_frame = s.size - end_skip
        s[:start_skip] = 0
        s[end_frame:] = 0
        self.sound = (s > self.threshold).astype(np.int_)
        
    def save_signal(self):
        
        base_name = self.signal_file.removesuffix('_signal.avi')
        sound_name = base_name + '_sound.csv'
        self.sound.to_csv(sound_name, index=False, header=False)
        
    def show_signal_thresholding(self, show=True, save=True):
        
        display.sound_analysis(self.signal_file, 
                               self.time_seconds, 
                               self.averages, 
                               self.n_highs, 
                               self.bin_sound, 
                               self.threshold, 
                               show=show, 
                               save=save)

 
            

