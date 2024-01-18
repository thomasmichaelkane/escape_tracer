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
from lib.signal_reader import SignalReader
from lib.settings import settings, dimensions

def main():
    
    FILENAME, THRESHOLD, START_IGNORE, END_IGNORE = parse_args()
    
    sr = SignalReader(FILENAME, dim=dimensions["signal_size"], fps=settings["fps"])
    sr.read()
    sr.threshold_signal(THRESHOLD, start_skip=START_IGNORE, end_skip=END_IGNORE)
    sr.save_signal()
    sr.show_signal_thresholding()

def parse_args():

    if len(sys.argv) == 1:
        
        raise KeyError("No file specified")
    
    elif len(sys.argv) == 2:
        
        filename = parse.videoname(sys.argv[1])
        threshold = 40
        start_ignore = 500
        end_ignore = 0
        
    elif len(sys.argv) == 3:
        
        filename = parse.videoname(sys.argv[1])
        threshold = parse.threshold(sys.argv[2])
        start_ignore = 500
        end_ignore = 0
    
    elif len(sys.argv) == 4:
        
        filename = parse.videoname(sys.argv[1])
        threshold = parse.threshold(sys.argv[2])
        start_ignore = parse.frame_ignore(sys.argv[3])
        end_ignore = 0
        
    
    elif len(sys.argv) == 5:
        
        filename = parse.videoname(sys.argv[1])
        threshold = parse.threshold(sys.argv[2])
        start_ignore = parse.frame_ignore(sys.argv[3])
        end_ignore = parse.frame_ignore(sys.argv[4])
            
    else:
        
        raise KeyError("Too many input arguments")
    
    return filename, threshold, start_ignore, end_ignore

    # time_seconds, averages, n_highs = sound.read_signal(FILENAME)
    # bin_sound = sound.get_binary(FILENAME, n_highs, START_IGNORE, END_IGNORE, THRESHOLD)
    # display.sound_analysis(FILENAME, time_seconds, averages, n_highs, bin_sound, THRESHOLD, show=True)

main()