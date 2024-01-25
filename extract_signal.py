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
from lib.obj.signal_reader import SignalReader

def main():
    
    SETTINGS = parse.load_config()
    
    FILENAME = parse_args()
    
    sr = SignalReader(FILENAME, 
                      SETTINGS["dimensions"]["signal"], 
                      SETTINGS["video"]["fps"], 
                      SETTINGS["signal"]["threshold"], 
                      SETTINGS["signal"]["start_frame"],
                      SETTINGS["signal"]["end_frame"])
    
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

main()