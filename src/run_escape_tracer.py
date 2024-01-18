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

from lib import parse
from lib.escape_tracer import EscapeTracer
from lib.settings import settings, dimensions

def main():
    
    FOLDER = parse_args()
    
    TRACKING_FILE, STIM_FILE = parse.get_file_names(FOLDER)
    
    et = EscapeTracer(TRACKING_FILE, settings, dimensions)
    et.load_stim_file(STIM_FILE)
    
    et.calc_speeds()
    et.global_displays()
    et.event_displays()
    et.output_report()

def parse_args():

    if len(sys.argv) == 1:
        
        raise KeyError("tracking and sound files must be specified")
    
    elif len(sys.argv) == 2:
        
        folder = parse.folder(sys.argv[1])
            
    else:
        
        raise KeyError("Too many input arguments")
    
    return folder


main()