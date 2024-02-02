import os

def threshold(arg):
    
    try:
        
        threshold = int(arg)
        
        return threshold
        
    except TypeError as e:
        
        print(e)

def frame_ignore(arg):
    
    try:
        
        frame_ignore = int(arg)
        
        return frame_ignore
        
    except TypeError as e:
        
        print(e)

def text_file(arg):
    
    if arg.endswith(".txt"):
        
        try:
            file = open(arg)
            file.close()
            return arg
        except FileNotFoundError as err:
            print(err)
            
    else:
        
        raise NameError("The file should be a .txt file")

def video_file(arg):
    
    if arg.endswith(".avi"):
        
        try:
            file = open(arg)
            file.close()
            return arg
        except FileNotFoundError as err:
            print(err)
            
    else:
        
        raise NameError("Needs to be an .avi file")
    
def h5_file(arg):
    
    if arg.endswith(".h5"):
        
        try:
            file = open(arg)
            file.close()
            return arg
        except FileNotFoundError as err:
            print(err)
            
    else:
        
        raise NameError("Needs to be an .h5 file")
    
def csv_file(arg):
    
    if arg.endswith(".csv"):
        
        try:
            file = open(arg)
            file.close()
            return arg
        except FileNotFoundError as err:
            print(err)
            
    else:
        
        raise NameError("Needs to be a .csv file")
    
def folder(arg):
    
    if os.path.isdir(arg):
        
        return arg
            
    else:
        
        raise NameError("Needs to be directory path")
    
def get_data_folders(parent_folder):
    
    data_folders = {folder_name: os.path.join(parent_folder, folder_name) for folder_name in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, folder))}
    
    return data_folders
    
def get_filenames(folder):
    
    all_paths = [os.path.join(folder, file) for file in os.listdir(folder) if os.path.isfile(os.path.join(folder, file))]
    tracking_file = stim_file = None

    for file in all_paths:
        
        if file.endswith(".h5"):
            tracking_file = h5_file(file)
            
        if file.endswith("_stim.csv") or file.endswith("_sound.csv"): # sound csv legacy
            stim_file = csv_file(file)
    
    if tracking_file is not None:
        return tracking_file, stim_file
    else:
        raise NameError("Tracking file required")
    
def get_video_file(folder):
    
    all_paths = [os.path.join(folder, file) for file in os.listdir(folder) if os.path.isfile(os.path.join(folder, file))]
    video_file = None

    for file in all_paths:

        if file.endswith("_arena.avi"):
            video_file = video_file(file)
            base_path = file.removesuffix("_arena.avi")
            
    if video_file is not None:
        return video_file, base_path
    else:
        raise NameError("No arena video file in folder")    