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

from escape_tracer.utils import parse, remove_indexed_folders
from escape_tracer import EscapeTracer, config

def run():
    
    FOLDER, INDEX_FILE = parse_args()
    
    data_folders = parse.get_data_folders(FOLDER)
    
    if INDEX_FILE is not None:

        data_folders = remove_indexed_folders(data_folders, INDEX_FILE)

    for folder_name, path in track(data_folders.items(), description="Analysing tracking data for multiple videos..."):
        
        try:
        
            processed_folder = os.path.join(path, "processed")
            
            tracking_file, stim_file = parse.get_filenames(processed_folder)
            
            et = EscapeTracer(tracking_file, config)
            et.load_stim_file(stim_file)
            et.load_background_image(config["tracking"]["background_image"])
            et.increase_fig_size()
            et.draw_global_traces()
            et.draw_event_traces() 
            et.save_speeds()
            et.save_pdf_report()
            
            print(f"Successfully processed {folder_name}")
            
        except:
            
            print(f"Error with video {folder_name}")

def parse_args():

    if len(sys.argv) == 1:
        
        raise KeyError("tracking, sound, and video files must be specified")
    
    elif len(sys.argv) == 2:
        
        folder = parse.folder(sys.argv[1])
        index_file = None
        
    elif len(sys.argv) == 3:
        
        folder = parse.folder(sys.argv[1])
        index_file = parse.text_file(sys.argv[2])      
             
    else:
        
        raise KeyError("Too many input arguments")
    
    return folder, index_file


if __name__ == "__main__":
    run()