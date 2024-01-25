import os
import cv2
from rich.progress import track
from rich import print as rprint

def get_frame(video_name):
    
    video = cv2.VideoCapture(video_name)
    
    for _ in range(500):
        
        _, frame = video.read()
                
    video.release()
    
    return frame

def save_segmentation_tif(folder, video_name, segmentation):
    
    base_name = video_name.removesuffix('.avi')
    segmentation_path = os.path.join(folder, base_name + '_segmentation.tif')
    
    cv2.imwrite(segmentation_path, segmentation)

def check_placements(frame, signal_coords, exit_coords, dimensions, thumbnail_scale):
    
    sx0, sx1, sy0, sy1 = get_signal_rectangle(signal_coords, dimensions)
    ax0, ax1, ay0, ay1 = get_relative_rectangle(exit_coords, dimensions["arena"])
    ex0, ex1, ey0, ey1 = get_relative_rectangle(exit_coords, dimensions["exit"])

    cv2.rectangle(frame,(sx0,sy0),(sx1,sy1),(0,0,255),3)
    cv2.rectangle(frame,(ax0,ay0),(ax1,ay1),(255,0,0),3)
    cv2.rectangle(frame,(ex0,ey0),(ex1,ey1),(0,255,0),3)

    # displaying the image
    small_frame = cv2.resize(frame, (int(round(frame.shape[1]*thumbnail_scale)), 
                                     int(round(frame.shape[0]*thumbnail_scale))))
    
    cv2.imshow("Confirm? yes [ENTER], exit [ESC], repeat [ANY]", small_frame)
  
    # wait for a key to be pressed to exit
    key = cv2.waitKey(0)
    
    cv2.destroyAllWindows()
    
    return key, frame
     
def get_exit(frame, thumbnail_scale):
    
    ex, ey = get_user_loc("Place coordinate on exit centre", frame, thumbnail_scale)
    
    rprint("Exit coordinates: ", ex, " ", ey)
    
    return (ex, ey)
    
    
def get_signal(frame, thumbnail_scale):
    
    sx, sy = get_user_loc("Place coordinate on signal", frame, thumbnail_scale)
    
    rprint("Signal coordinates: ", sx, " ", sy)
    
    return (sx, sy)
                
def get_user_loc(msg, frame, thumbnail_scale):
  
    # displaying the image
    small_frame = cv2.resize(frame, 
                             (int(round(frame.shape[1]*thumbnail_scale)), 
                              int(round(frame.shape[0]*thumbnail_scale)))
                             )
    
    cv2.imshow(msg, small_frame)
  
    # setting mouse handler for the image and calling the click_event() function
    global click_x, click_y
    cv2.setMouseCallback(msg, click_event)
  
    # wait for a key to be pressed to exit
    cv2.waitKey(0)
    
    cv2.destroyAllWindows()
    
    x = int(round(click_x/thumbnail_scale))
    y = int(round(click_y/thumbnail_scale))
    
    return (x, y)

# function to display the coordinates of of the points clicked on the image 
def click_event(event, x, y, flags, params):
  
    global click_x, click_y
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
  
        rprint(x, " ", y, end='\r')
        # displaying the coordinates on the Shell
        click_x, click_y = x, y

def get_signal_rectangle(signal_coords, dimensions):
    
    sx, sy = signal_coords
    sx0 = int(sx - dimensions["signal"][0]/2)
    sx1 = int(sx + dimensions["signal"][0]/2)
    sy0 = int(sy - dimensions["signal"][1]/2)
    sy1  = int(sy + dimensions["signal"][1]/2)
    
    return sx0, sx1, sy0, sy1

def get_relative_rectangle(exit_coords, relative_dimensions):
    
    ex, ey = exit_coords
    x0 = ex - relative_dimensions[0]
    x1 = ex + relative_dimensions[2]
    y0 = ey - relative_dimensions[1]
    y1 = ey + relative_dimensions[3]
    
    return x0, x1, y0, y1

def segment_video(folder, video_path, signal_coords, exit_coords, dimensions, video_settings):
    
    video_name = os.path.basename(video_path)
    base_name = video_name.removesuffix('.avi')
    
    signal_path = os.path.join(folder, base_name + '_signal.avi')
    sx0, sx1, sy0, sy1 = get_signal_rectangle(signal_coords, dimensions)
    dim_signal_x = dimensions["signal"][0]
    dim_signal_y = dimensions["signal"][1]

    arena_path = os.path.join(folder, base_name + '_arena.avi')   
    ax0, ax1, ay0, ay1 = get_relative_rectangle(exit_coords, dimensions["arena"])  
    dim_arena_x = ax1 - ax0
    dim_arena_y = ay1 - ay0
    
    video = cv2.VideoCapture(video_path)
    n_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    signal = cv2.VideoWriter(signal_path, 
                             cv2.VideoWriter_fourcc('M','J','P','G'), 
                             video_settings["fps"], 
                             (dim_signal_x, dim_signal_y))
    
    arena = cv2.VideoWriter(arena_path, 
                            cv2.VideoWriter_fourcc('M','J','P','G'), 
                            video_settings["fps"], 
                            (dim_arena_x, dim_arena_y))
    
    for _ in track(range(n_frames), description="Segmenting video..."):
        
        ret, frame = video.read()
        
        if ret:
            
            # Press Q on keyboard to  exit
            if cv2.waitKey(0) & 0xFF == ord('q'):
                break

            # if frameno > signal_start_frame:
            signal_frame = frame[sy0:sy1, sx0:sx1]
            signal.write(signal_frame)
            
            arena_frame = frame[ay0:ay1, ax0:ax1]
            arena.write(arena_frame)
            
        else:
            
            break

    video.release()
    signal.release()
    arena.release()
    
    cv2.destroyAllWindows()