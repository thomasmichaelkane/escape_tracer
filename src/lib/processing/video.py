import os
import cv2
from ..settings.settings import video_settings, dimensions
from rich.progress import track
from rich import print as rprint

def get_frame(video_name):
    
    video = cv2.VideoCapture(video_name)
    
    for _ in range(500):
        
        _, frame = video.read()
                
    video.release()
    
    return frame

def save_segmentation(folder, video_name, segmentation):
    
    base_name = video_name.removesuffix('.avi')
    segmentation_path = os.path.join(folder, base_name + '_segmentation.tif')
    
    cv2.imwrite(segmentation_path, segmentation)

def check_placements(frame, signal_coords, exit_coords):
    
    sx0, sx1, sy0, sy1 = get_signal_rectangle(signal_coords)
    ax0, ax1, ay0, ay1 = get_arena_rectangle(exit_coords)
    ex0, ex1, ey0, ey1 = get_exit_rectangle(exit_coords)

    cv2.rectangle(frame,(sx0,sy0),(sx1,sy1),(0,0,255),3)
    cv2.rectangle(frame,(ax0,ay0),(ax1,ay1),(255,0,0),3)
    cv2.rectangle(frame,(ex0,ey0),(ex1,ey1),(0,255,0),3)

    # displaying the image
    small_frame = cv2.resize(frame, (int(round(frame.shape[1]*video_settings["view_scale"])), 
                                     int(round(frame.shape[0]*video_settings["view_scale"]))))
    
    cv2.imshow("Confirm? yes [ENTER], exit [ESC], repeat [ANY]", small_frame)
  
    # wait for a key to be pressed to exit
    key = cv2.waitKey(0)
    
    cv2.destroyAllWindows()
    
    return key, frame
     
def get_exit(frame):
    
    ex, ey = get_user_loc("Place coordinate on exit centre", frame)
    
    rprint("Exit coordinates: ", ex, " ", ey)
    
    return (ex, ey)
    
    
def get_signal(frame):
    
    sx, sy = get_user_loc("Place coordinate on signal", frame)
    
    rprint("Signal coordinates: ", sx, " ", sy)
    
    return (sx, sy)
                
def get_user_loc(msg, frame):
  
    # displaying the image
    small_frame = cv2.resize(frame, (int(round(frame.shape[1]*video_settings["view_scale"])), 
                                     int(round(frame.shape[0]*video_settings["view_scale"]))))
    
    cv2.imshow(msg, small_frame)
  
    # setting mouse handler for the image
    # and calling the click_event() function
    global click_x, click_y
    cv2.setMouseCallback(msg, click_event)
  
    # wait for a key to be pressed to exit
    cv2.waitKey(0)
    
    cv2.destroyAllWindows()
    
    x = int(round(click_x/video_settings["view_scale"]))
    y = int(round(click_y/video_settings["view_scale"]))
    
    return (x, y)



# function to display the coordinates of
# of the points clicked on the image 
def click_event(event, x, y, flags, params):
  
    global click_x, click_y
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
  
        rprint(x, " ", y, end='\r')
        # displaying the coordinates on the Shell
        click_x, click_y = x, y

def get_signal_rectangle(signal_coords):
    
    sx, sy = signal_coords
    sx0 = int(sx - dimensions["signal_size"][0]/2)
    sx1 = int(sx + dimensions["signal_size"][0]/2)
    sy0 = int(sy - dimensions["signal_size"][1]/2)
    sy1  = int(sy + dimensions["signal_size"][1]/2)
    
    return sx0, sx1, sy0, sy1

def get_arena_rectangle(exit_coords):
    
    ex, ey = exit_coords
    ax0 = ex - dimensions["arena_left"]
    ax1 = ex + dimensions["arena_right"]
    ay0 = ey - dimensions["arena_top"]
    ay1 = ey + dimensions["arena_bottom"]
    
    return ax0, ax1, ay0, ay1

def get_exit_rectangle(exit_coords):
    
    ex, ey = exit_coords
    ex0 = ex - dimensions["exit_left"]
    ex1 = ex + dimensions["exit_top"]
    ey0 = ey - dimensions["exit_right"]
    ey1 = ey + dimensions["exit_bottom"]
    
    return ex0, ex1, ey0, ey1

def chop_video(folder, video_path, signal_coords, exit_coords):
    
    video_name = os.path.basename(video_path)
    base_name = video_name.removesuffix('.avi')
    
    signal_path = os.path.join(folder, base_name + '_signal.avi')
    sx0, sx1, sy0, sy1 = get_signal_rectangle(signal_coords)
    dim_signal_x = dimensions["signal_size"][0]
    dim_signal_y = dimensions["signal_size"][1]

    arena_path = os.path.join(folder, base_name + '_arena.avi')   
    ax0, ax1, ay0, ay1 = get_arena_rectangle(exit_coords)  
    dim_arena_x = ax1 - ax0
    dim_arena_y = ay1 - ay0

    fps = video_settings["fps"]
    
    video = cv2.VideoCapture(video_path)
    n_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    signal = cv2.VideoWriter(signal_path, 
                             cv2.VideoWriter_fourcc('M','J','P','G'), 
                             fps, 
                             (dim_signal_x, dim_signal_y))
    
    arena = cv2.VideoWriter(arena_path, 
                            cv2.VideoWriter_fourcc('M','J','P','G'), 
                            fps, 
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
    
    
    
    
    
    
    # signalx_start = 60
    # signalx_end = 135
    # signaly_start = 185
    # signaly_end = 260
    # dim_signal_x = signalx_end _ signalx_start
    # dim_signal_y = signaly_end _ signaly_start
    
    # sx, sy = signal_xy[0]*shrink, signal_xy[1]*shrink
    # ex, ey = exit_xy[0]*shrink, exit_xy[1]*shrink

    # x0 = 394
    # x1 = 1414
    # y0 = 0
    # y1 = 833
