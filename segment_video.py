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

from lib.obj.video_segmenter import VideoSegmenter
from lib.utils import parse

def main():
    
    SETTINGS = parse.load_config()
    
    VIDEO_PATH = parse_args()
    
    vc = VideoSegmenter(VIDEO_PATH, SETTINGS)
    vc.segment()
    
def parse_args():

    if len(sys.argv) == 1:
        raise KeyError("No file specified")

    elif len(sys.argv) == 2:
        filename = parse.video_file(sys.argv[1])
                      
    else:
        raise KeyError("Too many input arguments")
    
    return filename

main()
