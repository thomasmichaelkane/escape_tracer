import os
import csv
import yaml
from datetime import datetime
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

def keep_indexed_folders(data_folders, index_file):
    with open(index_file) as file:
        indices = file.readlines()
        indices = [index.strip() for index in indices]

    keys_to_remove = [key for key in data_folders if key not in indices]

    for key in keys_to_remove:
        data_folders.pop(key)
        
    for key in data_folders.keys():
        print(f"Loading {key} via index file")

    return data_folders
    

def load_config():
    
    with open('config.yaml') as config:
        settings = yaml.load(config.read(), Loader=yaml.Loader)
        
    return settings

def load_stim_file(tracking_file):
    
    folder = os.path.dirname(tracking_file)

    all_paths = [os.path.join(folder, file) for file in os.listdir(folder) if os.path.isfile(os.path.join(folder, file))]
    stim_file = None

    for file in all_paths:
        
        if file.endswith("_stim.csv") or file.endswith("_sound.csv"): # sound csv legacy
            stim_file = file
    
    return stim_file

def read_tracking_file(tracking_file):
    
    tracking = pd.read_hdf(tracking_file)
    
    return tracking

def create_folder(base_folder, name, append_date=True):
    
    if append_date:
        now = datetime.now()
        time = now.strftime("_%Y-%m-%d_%H-%M-%S")
        name = name + time
    
    new_folder = os.path.join(base_folder, name)
        
    os.mkdir(new_folder)
    return new_folder

def create_csv(list, filename):
    
    with open(filename, 'w', newline='') as file:
        
        writer = csv.writer(file)
        
        for row in list:
            if row[1] is None:
                row = [row[0], "None", "None"]
            writer.writerow(row)
            
def save_report(figs, base_path):
    
    with PdfPages(base_path + '_report.pdf') as pdf:

        for fig in figs:
            pdf.savefig(fig)