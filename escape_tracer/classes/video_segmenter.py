import os

from escape_tracer.utils import logging
from escape_tracer.processing import video

class VideoSegmenter():
    def __init__(self, video_file, settings):
        
        self.video_file = video_file
        self.settings = settings

        folder, self.name = os.path.split(video_file)
        parent_folder = os.path.dirname(folder)
        self.processed_folder = os.path.join(parent_folder, "processed")
        
        try: 
            os.mkdir(self.processed_folder)
        except:
            print("processed dir already exists")
        
        self.blank_frame = video.get_frame(video_file)
        
    def segment(self):
        
        key = None
        
        while (key != 13) & (key != 27): # enter/escape key
            
            frame = self.blank_frame.copy()
            signal_coords = video.get_signal(frame, self.settings["video"]["thumbnail_scale"])
            exit_coords = video.get_exit(frame, self.settings["video"]["thumbnail_scale"])
            logging.display_coords(signal_coords, exit_coords)
            
            key, segments = video.check_placements(frame, 
                                                   signal_coords, 
                                                   exit_coords, 
                                                   self.settings["dimensions"], 
                                                   self.settings["video"]["thumbnail_scale"])
        
        if key == 13:
            
            video.save_segmentation_tif(self.processed_folder, self.name, segments)
            
            video.segment_video(self.processed_folder, 
                                self.video_file, 
                                signal_coords, 
                                exit_coords, 
                                self.settings["dimensions"], 
                                self.settings["video"])