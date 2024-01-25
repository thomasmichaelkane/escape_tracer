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

def main():
    
    FOLDER = parse_args()
    
    SETTINGS = parse.load_config()
    
    data_folders = parse.get_data_folders(FOLDER)
    
    for folder in track(data_folders, description="Analysing tracking data for multiple videos..."):
        
        processed_folder = os.path.join(folder, "processed")
        
        TRACKING_FILE, STIM_FILE = parse.get_filenames(processed_folder)
        
        et = EscapeTracer(TRACKING_FILE, SETTINGS)
        # et.load_stim_file(STIM_FILE)
        et.load_background_image(SETTINGS["tracking"]["background_image"])
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
            
    else:
        
        raise KeyError("Too many input arguments")
    
    return folder


main()