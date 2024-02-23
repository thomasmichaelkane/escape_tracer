import sys
import os
from rich.progress import track

from escape_tracer.utils import parse, collation, keep_indexed_folders

def run():
    
    FOLDER, INDEX_FILE = parse_args()
    
    data_folders = parse.get_data_folders(FOLDER)
    meta_data = {}
    speeds_data = {}
    locs_data = {}
    averages_data = {}
    
    if INDEX_FILE is not None:

        data_folders = keep_indexed_folders(data_folders, INDEX_FILE)
        output_folder = os.path.dirname(INDEX_FILE)
        
    else:
        
        output_folder = FOLDER
        print("Loading all folders...")

    for folder_name, path in track(data_folders.items(), description="Collating events data..."):
        
        if collation.check_for_events(path):
        
            try:

                meta, speeds, locs, average_speeds = collation.read_event_data(path, folder_name)
                
                meta_data.update(meta)
                speeds_data.update(speeds)
                locs_data.update(locs)
                averages_data[folder_name] = average_speeds
                
                print(f"Successfully collated {folder_name}")
                
            except:
                
                print(f"Error with {folder_name}")
                
        else:
            
            print(f"No events for {folder_name}")
        
        collated_meta_path = os.path.join(output_folder, "collated_escape-stats.csv")
        collation.write_collated_data(collated_meta_path, meta_data)
        
        collated_speeds_path = os.path.join(output_folder, "collated_speeds.csv")
        collation.write_collated_data(collated_speeds_path, speeds_data)
        
        collated_locs_path = os.path.join(output_folder, "collated_locs.csv")
        collation.write_collated_data(collated_locs_path, locs_data)
        
        collated_averages_path = os.path.join(output_folder, "collated_average-speeds.csv")
        collation.write_collated_data(collated_averages_path, averages_data)
        
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