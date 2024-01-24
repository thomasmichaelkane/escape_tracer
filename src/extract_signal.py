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
from lib.settings.settings import video_settings, signal_settings, dimensions

def main():
    
    FILENAME, THRESHOLD, START_SKIP, END_SKIP = parse_args()
    
    sr = SignalReader(FILENAME, dimensions["signal_size"], video_settings["fps"], THRESHOLD, START_SKIP, END_SKIP)
    sr.threshold_with_user_confirmation()
    sr.save()

def parse_args():

    if len(sys.argv) == 1:
        
        raise KeyError("No file specified")
    
    elif len(sys.argv) == 2:
        
        filename = parse.videoname(sys.argv[1])
        threshold = signal_settings["default_threshold"]
        start_skip = signal_settings["default_start_skip"]
        end_skip = signal_settings["default_end_skip"]
        
    elif len(sys.argv) == 3:
        
        filename = parse.videoname(sys.argv[1])
        threshold = parse.threshold(sys.argv[2])
        start_skip = signal_settings["default_start_skip"]
        end_skip = signal_settings["default_end_skip"]
    
    elif len(sys.argv) == 4:
        
        filename = parse.videoname(sys.argv[1])
        threshold = parse.threshold(sys.argv[2])
        start_skip = parse.frame_skip(sys.argv[3])
        end_skip = signal_settings["default_end_skip"]
        
    
    elif len(sys.argv) == 5:
        
        filename = parse.videoname(sys.argv[1])
        threshold = parse.threshold(sys.argv[2])
        start_skip = parse.frame_skip(sys.argv[3])
        end_skip = parse.frame_skip(sys.argv[4])
            
    else:
        
        raise KeyError("Too many input arguments")
    
    return filename, threshold, start_skip, end_skip

    # time_seconds, averages, n_highs = sound.read_signal(FILENAME)
    # bin_sound = sound.get_binary(FILENAME, n_highs, START_skip, END_skip, THRESHOLD)
    # display.sound_analysis(FILENAME, time_seconds, averages, n_highs, bin_sound, THRESHOLD, show=True)

main()