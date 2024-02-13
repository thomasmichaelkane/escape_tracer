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

from escape_tracer import EscapeTracer, config, parse
from escape_tracer.utils import load_stim_file

def run():
    
    TRACKING_FILE = parse_args()
    STIM_FILE = load_stim_file(TRACKING_FILE)
    
    et = EscapeTracer(TRACKING_FILE, config)
    
    et.load_stim_file(STIM_FILE)
    et.load_background_image(config["tracking"]["background_image"])
    et.increase_fig_size()
    
    et.draw_global_traces()
    et.draw_event_traces()
    
    et.save_speeds()
    et.save_pdf_report()

def parse_args():

    if len(sys.argv) == 1:
        
        raise KeyError("tracking file must be specified")
    
    elif len(sys.argv) == 2:
        
        folder = parse.h5_file(sys.argv[1])
            
    else:
        
        raise KeyError("Too many input arguments")
    
    return folder

if __name__ == "__main__":
    run()