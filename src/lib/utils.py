import os
import csv
from datetime import datetime
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

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