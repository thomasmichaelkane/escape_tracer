import os
import csv
import numpy as np

def read_event_data(data_folder_path, data_folder_name):
    
    analysis_folder = os.path.join(data_folder_path, "analysis")
    et_output_folder = os.path.join(analysis_folder, os.listdir(analysis_folder)[0])
    
    files_list = os.listdir(et_output_folder)
    
    meta_file_name = [file for file in files_list if file.endswith("escape-stats.csv")][0]
    meta_file_path = os.path.join(et_output_folder, meta_file_name)

    event_folders = [event_folder for event_folder in os.listdir(et_output_folder) if os.path.isdir(os.path.join(et_output_folder, event_folder))]    

    meta_dict = {}
    speeds_dict = {}
    locs_dict = {}
    all_event_speeds = []
    
    with open(meta_file_path, newline='') as metafile:
        metareader = csv.reader(metafile)
    
        for event_folder in event_folders:
            
            event_name = data_folder_name + "_" + event_folder
            
            event_folder_path = os.path.join(et_output_folder, event_folder)
            event_file = os.listdir(event_folder_path)[0]
            event_file_path = os.path.join(event_folder_path, event_file)
            
            meta_dict[event_name] = next(metareader)

            with open(event_file_path, newline='') as eventfile:
                eventreader = csv.reader(eventfile)
                
                next(eventreader)
                speeds = next(eventreader)
                speeds_dict[event_name] = speeds
                locs_dict[event_name] = next(eventreader)
                
                all_event_speeds.append(np.array([float(speed) for speed in speeds]))
    
    average_speeds = np.array(all_event_speeds).mean(axis=0)
    
    return meta_dict, speeds_dict, locs_dict, average_speeds

def write_collated_data(path, data):
    
    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
    
        # Write the header row
        writer.writerow(data.keys())
        
        # Write the data rows
        writer.writerows(zip(*data.values()))