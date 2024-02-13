import sys
import os
from rich.progress import track

from escape_tracer.utils import parse, collation, keep_indexed_folders

def run():
    
    FOLDER, INDEX_FILE = parse_args()
    
    data_folders = parse.get_data_folders(FOLDER)
    speeds_data = {}
    locs_data = {}
    
    if INDEX_FILE is not None:

        data_folders = keep_indexed_folders(data_folders, INDEX_FILE)

    for folder_name, path in track(data_folders.items(), description="Collating events data..."):
        
        try:
        
            speeds, locs = collation.read_event_data(path, folder_name)
            
            speeds_data.update(speeds)
            locs_data.update(locs)
            
            print(f"Successfully collated {folder_name}")
            
        except:
            
            print(f"Error with dataset {folder_name}")
        
        collated_speeds_path = os.path.join(FOLDER, "collated_speeds.csv")
        # collated_locs_path = os.path.join(FOLDER, "collated_locs.csv")
        
        collation.write_collated_data(collated_speeds_path, speeds_data)
        # collation.write_collated_data(collated_locs_path, locs_data)

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