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

from escape_tracer.utils import parse
from escape_tracer import SignalReader, config

def run():
    
    FILENAME = parse_args()
    
    sr = SignalReader(FILENAME, 
                      dim=config["dimensions"]["signal"], 
                      fps=config["video"]["fps"], 
                      threshold=config["signal"]["threshold"], 
                      start_frame=config["signal"]["start_frame"],
                      end_frame=config["signal"]["end_frame"])
    
    sr.threshold_with_user_confirmation()
    sr.save()

def parse_args():

    if len(sys.argv) == 1:
        
        raise KeyError("No file specified")
    
    elif len(sys.argv) == 2:
        
        filename = parse.video_file(sys.argv[1])
            
    else:
        
        raise KeyError("Too many input arguments")
    
    return filename

run()