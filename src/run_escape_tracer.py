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

from lib.utils import parse
from lib.obj.escape_tracer import EscapeTracer
from lib.settings.settings import video_settings, dimensions

def main():
    
    FOLDER = parse_args()
    
    TRACKING_FILE, STIM_FILE = parse.get_file_names(FOLDER)
    
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
        
        raise KeyError("tracking and sound files must be specified")
    
    elif len(sys.argv) == 2:
        
        folder = parse.folder(sys.argv[1])
            
    else:
        
        raise KeyError("Too many input arguments")
    
    return folder


main()