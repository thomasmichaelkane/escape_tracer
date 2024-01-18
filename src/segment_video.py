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

from lib import video, parse, logging

def main():
    
    VIDEO_PATH = parse_args()
    folder, name = os.path.split(VIDEO_PATH)
    parent_folder = os.path.dirname(folder)
    processed_folder = os.path.join(parent_folder, "processed")
    
    try: 
        os.mkdir(processed_folder)
    except:
        print("processed dir already exists")
    
    frame = video.get_frame(VIDEO_PATH)
    
    key = None
    
    while (key != 13) & (key != 27): # enter/escape key
        signal_coords = video.get_signal(frame)
        exit_coords = video.get_exit(frame)
        logging.display_coords(signal_coords, exit_coords)
        key, segments = video.check_placements(frame, signal_coords, exit_coords)
    
    if key == 13:
        video.save_segmentation(processed_folder, name, segments)
        video.chop_video(processed_folder, VIDEO_PATH, signal_coords, exit_coords)

def parse_args():

    if len(sys.argv) == 1:
        raise KeyError("No file specified")

    elif len(sys.argv) == 2:
        filename = parse.videoname(sys.argv[1])
                      
    else:
        raise KeyError("Too many input arguments")
    
    return filename

main()
