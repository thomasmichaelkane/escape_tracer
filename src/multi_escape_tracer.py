"""---

---

Example
-------
-----

    $ python -----

Notes
-----
    -------


Arguments
----------
--- : str
    -----.

--- : float
    ----
    
"""

import sys
import os
from rich.progress import track

from lib.utils import parse
from lib.obj.escape_tracer import EscapeTracer
from lib.settings.settings import video_settings, dimensions

def main():
    
    DATA_FOLDER = parse_args()
    
    folders = [os.path.join(DATA_FOLDER, folder) for folder in os.listdir(DATA_FOLDER) if os.path.isdir(os.path.join(DATA_FOLDER, folder))]
    
    for folder in track(folders, description="Analysing tracking data..."):
        
        processed_folder = os.path.join(folder, "processed")
        
        TRACKING_FILE, STIM_FILE = parse.get_file_names(processed_folder)
        
        et = EscapeTracer(TRACKING_FILE, video_settings, dimensions)
        et.load_stim_file(STIM_FILE)
        et.load_background_image(video_settings["background_image"])
        et.increase_fig_size()
        et.draw_global_traces()
        et.draw_event_traces() 
        et.save_speeds()
        et.save_pdf_report()

def parse_args():

    if len(sys.argv) == 1:
        
        raise KeyError("tracking, sound, and video files must be specified")
    
    elif len(sys.argv) == 2:
        
        folder = parse.folder(sys.argv[1])
    
    # elif len(sys.argv) == 4:
        
    #     tracking_file = parse.h5name(sys.argv[1])
    #     sound_file = parse.csvname(sys.argv[2])
    #     video_file = parse.videoname(sys.argv[3])
            
    else:
        
        raise KeyError("Too many input arguments")
    
    # return tracking_file, sound_file, video_file
    return folder


main()