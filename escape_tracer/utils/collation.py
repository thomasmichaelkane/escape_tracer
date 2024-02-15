import os
import csv
import numpy as np

def read_event_data(data_folder_path, data_folder_name):
    
    analysis_folder = os.path.join(data_folder_path, "analysis")
    et_output_folder = os.path.join(analysis_folder, os.listdir(analysis_folder)[0])

    event_folders = [event_folder for event_folder in os.listdir(et_output_folder) if os.path.isdir(os.path.join(et_output_folder, event_folder))]    

    speeds_dict = {}
    locs_dict = {}
    
    for event_folder in event_folders:
        
        event_name = data_folder_name + "_" + event_folder
        
        event_folder_path = os.path.join(et_output_folder, event_folder)
        event_file = os.listdir(event_folder_path)[0]
        event_file_path = os.path.join(event_folder_path, event_file)

        with open(event_file_path, newline='') as csvfile:
            eventreader = csv.reader(csvfile)
            
            next(eventreader)
            speeds = next(eventreader)
            locs = next(eventreader)
            
            speeds_dict[event_name] = speeds
            locs_dict[event_name] = locs
            
    speeds_average = [np.mean(event_speeds) for event_speeds in speeds_dict.items()]
        
        
      
    return speeds_dict, locs_dict

def write_collated_data(path, data):
    
    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
    
        # Write the header row
        writer.writerow(data.keys())
        
        # Write the data rows
        writer.writerows(zip(*data.values()))