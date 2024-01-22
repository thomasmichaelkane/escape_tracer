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

# def fix(arg):
    
#     try:
        
#         start_frame = int(arg)
        
#         return start_frame
        
#     except TypeError as e:
        
#         print(e)

def videoname(arg):
    
    if arg.endswith(".avi"):
        
        try:
            file = open(arg)
            file.close()
            return arg
        except FileNotFoundError as err:
            print(err)
            
    else:
        
        raise NameError("Needs to be an .avi file")
    
def h5name(arg):
    
    if arg.endswith(".h5"):
        
        try:
            file = open(arg)
            file.close()
            return arg
        except FileNotFoundError as err:
            print(err)
            
    else:
        
        raise NameError("Needs to be an .h5 file")
    
def csvname(arg):
    
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
    
def get_file_names(folder):
    
    all_paths = [os.path.join(folder, file) for file in os.listdir(folder) if os.path.isfile(os.path.join(folder, file))]
    tracking_file = sound_file = None

    for file in all_paths:
        
        if file.endswith(".h5"):
            tracking_file = h5name(file)
            
        if file.endswith("_sound.csv"):
            sound_file = csvname(file)
            
        # if file.endswith("_exit.csv"):
        #     exit_file = csvname(file)
    
    if tracking_file is not None: # and exit_file is not None:
        return tracking_file, sound_file#, exit_file
    else:
        raise NameError("Tracking file required")
    
def get_video_name(folder):
    
    all_paths = [os.path.join(folder, file) for file in os.listdir(folder) if os.path.isfile(os.path.join(folder, file))]
    video_file = None

    for file in all_paths:

        if file.endswith("_arena.avi"):
            video_file = videoname(file)
            base_path = file.removesuffix("_arena.avi")
            
    if video_file is not None:
        return video_file, base_path
    else:
        raise NameError("No arena video file in folder")    