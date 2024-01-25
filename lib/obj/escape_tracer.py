import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from ..processing import display, arena, stats, stim
from ..utils.utils import *

class EscapeTracer():
    def __init__(self, tracking_file, settings, save_figs=False):
        
        for k, v in settings["video"].items():
            setattr(self, k, v)
            
        for k, v in settings["tracking"].items():
            setattr(self, k, v)
     
        self.tracking_file = tracking_file
        self.tracking_db = read_tracking_file(self.tracking_file)  
        self.save_figs = save_figs 
         
        # time and event attributes
        self.num_frames = self.tracking_db.shape[0]
        frame_time = (1./self.fps)
        self.total_time = self.num_frames * frame_time
        self.time = np.arange(self.num_frames) * frame_time
        self.schedule = (self.event["t_minus"], self.event["length"], self.event["t_plus"])
        self.norm_event_time = np.arange(-self.event["t_minus"], (self.event["length"]+self.event["t_plus"]), frame_time) #############
        self.exit_roi = arena.get_exit_roi(settings["dimensions"])
        
        # read tracking data
        scorer = self.tracking_db.columns.get_level_values(0)[0]
        self.tracking = self.tracking_db[scorer][self.target_bodypart]
        self.detections = self.tracking['likelihood'].values > self.pcutoff
        self.tracking_detected = self.tracking[self.detections]
    
        self.folder, self.file_name = os.path.split(self.tracking_file)
        self.base_name = self.file_name.removesuffix('.h5')
    
        parent_folder = os.path.dirname(self.folder)
        self.analysis_folder = os.path.join(parent_folder, "analysis")
        
        try: 
            os.mkdir(self.analysis_folder)
        except:
            pass
        
        self.results_folder = create_folder(self.analysis_folder, "et_output")
        self.base_path = os.path.join(self.results_folder, self.base_name)
        
        # initialise figures list
        self.figs = []
        
        self.image_file = None
        self.stim_file = None
        self.stim_data = np.zeros(self.num_frames)
        
        self.calc_speeds()
        
    def load_stim_file(self, stim_file):
        
        self.stim_file = stim_file
        
        # read stim data
        if self.stim_file is not None:
            self.stim_data = stim.read_stim_file(self.stim_file, self.num_frames)
            self.stim_event_frames = stim.get_stim_events(self.stim_data)
            
    def load_background_image(self, image_file):
        
        self.image_file = image_file
        
    def increase_fig_size(self):
        
        plt.rcParams['figure.figsize'] = [14, 7]
        plt.rcParams["figure.autolayout"] = True   
        
    def calc_speeds(self):
        
        self.speeds, self.locs = stats.calculate_speeds(self.tracking, 
                                                  self.detections, 
                                                  self.num_frames, 
                                                  self.fps,
                                                  self.speed_cutoff,
                                                  self.exit_roi)

    def save_speeds(self, suffix='_speeds'):
        
        speed_tracking = pd.DataFrame((self.speeds, self.locs))
        speed_tracking.to_csv(self.base_path + suffix + '.csv')
        
        if self.stim_file is not None:
            
            for path, df in zip(self.event_base_paths, self.event_speed_dfs):
                df.to_csv(path + suffix + '.csv')
    
    def draw_global_traces(self, show=False):
        
        # trip grid
        self.trip_fig = display.trip_grid(self.tracking_detected, show=show)
        self.figs.append(self.trip_fig)
        plt.close()
        
        # # time plot
        self.time_fig, ax = plt.subplots()
        self.figs.append(self.time_fig)
        plt.title('Activity over time')
        
        display.time_plot_on_image(ax, 
                                   self.tracking,
                                   self.fps,
                                   self.pcutoff,
                                   image_file=self.image_file,
                                   length=self.total_time,
                                   show=show)
     
        # speed plot
        self.speed_fig, speed_ax = plt.subplots()
        self.figs.append(self.speed_fig)
        plt.title('Velocity')
        
        display.two_plots(self.speed_fig, 
                          speed_ax, 
                          self.time, 
                          self.speeds, 
                          self.stim_data,
                          x_label='Time (s)', 
                          data1_label='Mouse Velocity (pix/s)', 
                          data2_label='stim (on/off)',
                          show=show)   
        
    def draw_event_traces(self, show=False):
        
        if self.stim_file is not None:
        
            all_event_speeds = []
            event_stats = []
            
            self.event_base_paths = []
            self.event_speed_dfs = []

            for i, event_t0 in enumerate(self.stim_event_frames, 1):
                
                start = event_t0 - (self.event["t_minus"]*self.fps)
                stim_end = event_t0 + (self.event["length"]*self.fps)
                end = stim_end + (self.event["t_plus"]*self.fps)
                
                if end < (self.num_frames - (self.event["t_plus"]*self.fps)):
                    
                    event_name = 'event_' + str(i)
                    event_folder_name = create_folder(self.results_folder, event_name, append_date=False)
                    event_base_path = os.path.join(event_folder_name, self.base_name + "_" + event_name)
                    self.event_base_paths.append(event_base_path)
                
                    event_speeds = self.speeds[start:end]
                    event_locs = self.locs[start:end]
                    event_stim = self.stim_data[start:end]
                    event_tracking = self.tracking.loc[start:end]
                    post_stim_speeds = self.speeds[event_t0:end]

                    event_speed_df = pd.DataFrame((event_speeds, event_locs))
                    self.event_speed_dfs.append(event_speed_df)
                    
                    escape_time, max_speed = stats.find_escape_stats(post_stim_speeds, 
                                                                     self.fps, 
                                                                     self.min_escape_frames,
                                                                     self.max_escape_window)
                    
                    
                    event_stats.append([i, escape_time, max_speed])
                    event_fig, (speed_ax, time_ax) = plt.subplots(1, 2)
                    self.figs.append(event_fig)
                    
                    plt.title('Event #' + str(i))
                    
                    display.time_plot_on_image(time_ax, 
                                event_tracking, 
                                self.fps, 
                                self.pcutoff, 
                                image_file=self.image_file,
                                schedule=self.schedule,
                                show=False,
                                close=False)
                    
                    display.two_plots(event_fig, 
                                    speed_ax, 
                                    self.norm_event_time, 
                                    event_speeds, 
                                    event_stim,
                                    x_label='Time (s)', 
                                    data1_label='Mouse Velocity (pix/s)', 
                                    data2_label='stim (on/off)',
                                    show=show)
                    

                    
                    if show: plt.show()
                    
                    plt.close()
                                        
                    all_event_speeds.append(event_speeds)

            

            csv_name = self.base_path + "_event_stats.csv"
            create_csv(event_stats, csv_name)
        
            # average event displays
            average_speeds = np.array(all_event_speeds).mean(axis=0)
            avg_fig, ax = plt.subplots()
            self.figs.append(avg_fig)
            plt.title('Average event speed')
            
            display.two_plots(avg_fig, 
                            ax, 
                            self.norm_event_time, 
                            average_speeds, 
                            event_stim,
                            x_label='Time (s)', 
                            data1_label='Mouse Velocity (pix/s)', 
                            data2_label='stim (on/off)',
                            show=show)
            
            plt.close()
            
        else:
            print("Cannot make escape analysis as no stimulus file loaded")
        
    def save_pdf_report(self):
    
        if len(self.figs) > 0:
            save_report(self.figs, self.base_path)
        else:
            print("No traces have been made yet")

    
    
    
    
# def analyse(tracking_file, stim_file, exit_file):
    
#     fps = settings["fps"]
#     pcutoff = settings["pcutoff"]
#     target_bodypart = settings["target_bodypart"]
#     exit_size = settings["exit_size"]
#     dim = settings["dim"]
#     exit_std = settings["exit_std"]
#     t_minus = settings["t_minus"]
#     event_length = settings["event_length"]
#     t_plus = settings["t_plus"]
    
#     exit_loc = get_exit_loc(exit_file)
#     exit_roi = create_exit_roi(exit_size, exit_loc)
#     offset = get_arena_offset(exit_loc, exit_std)
    
#     # exit_roi = get_exit_roi()
    
#     # read tracking data
#     tracking_db = read_tracking_file(tracking_file)
     
#     num_frames = tracking_db.shape[0]
#     frame_time = (1./fps)
#     total_time = num_frames * frame_time
#     time = np.arange(num_frames) * frame_time
    
#     schedule = (t_minus, event_length, t_plus)
#     norm_event_time = np.arange(-t_minus, (event_length+t_plus), frame_time) #############
    
#     # read stim data
#     stim, source_dir, base_name = read_stim_file(stim_file, num_frames)
#     stim_event_frames = get_stim_events(stim)
    
#     results_folder = create_folder(source_dir, "B-Analysis")
#     base_path = os.path.join(results_folder, base_name)
    
#     # extract dataframe subsets
#     scorer = tracking_db.columns.get_level_values(0)[0]
#     bodyparts = list(dict.fromkeys(tracking_db.columns.get_level_values(1)))
#     tracking = tracking_db[scorer][target_bodypart]
#     detections = tracking['likelihood'].values > pcutoff
#     tracking_detected = tracking[detections]
    
#     speeds = calculate_speeds(tracking, detections, num_frames, fps, base_path, exit_roi)
#     figs = []
    
#     # global displays
#     all_bp_name = base_path + '_all_bp'
#     display.trip_grid(tracking_detected)
#     trip_fig = plt.gcf()
    
#     time_fig, ax = plt.subplots()
#     plt.title('Activity over time')
#     display.time_plot_on_image(ax, tracking, base_path, fps, length=total_time, pcutoff=pcutoff, offset=offset)
#     # display.dlc_plots(tracking_db, [target_bodypart], scorer, dim, all_bp_name, pcutoff=pcutoff)
    
#     speed_fig, ax = plt.subplots()
#     plt.title('Velocity')
#     display.two_plots(speed_fig, ax, time, speeds, stim, base_path, 'Time (s)', 'Mouse Velocity (pix/s)', 'stim (on/off)')

#     # event displays
#     all_event_speeds = []
#     event_stats = []
#     figs.append(trip_fig)
#     figs.append(time_fig)
    
#     for i, event_t0 in enumerate(stim_event_frames, 1):
        
#         start = event_t0 - (t_minus*fps)
#         stim_end = event_t0 + (event_length*fps)
#         end = stim_end + (t_plus*fps)
        
#         if end < (num_frames - (t_plus*fps)):
            
#             event_name = 'event_' + str(i)
#             event_folder_name = create_folder(results_folder, event_name, append_date=False)
#             event_base_path = os.path.join(event_folder_name, base_name + "_" + event_name)
        
#             event_time = time[start:end]
#             event_speeds = speeds[start:end]
#             event_stim = stim[start:end]
#             event_tracking = tracking.loc[start:end]
#             stim_on_speeds = speeds[event_t0:end]
        
#             event_speed_df = pd.DataFrame(event_speeds)
#             event_speed_df.to_csv(event_base_path + '_speeds.csv')
            
#             escape_time, max_speed = find_escape_stats(stim_on_speeds, fps)
#             event_stats.append([i, escape_time, max_speed])
#             event_fig, (ax1, ax2) = plt.subplots(1, 2)
#             figs.append(event_fig)
#             plt.title('Event #' + str(i))
#             display.time_plot_on_image(ax2, event_tracking, event_base_path, fps, pcutoff, schedule=schedule, offset=offset)
#             display.two_plots(event_fig, ax1, norm_event_time, event_speeds, event_stim, event_base_path, 'Time (s)', 'Mouse Velocity (pix/s)', 'stim (on/off)') 
#             all_event_speeds.append(event_speeds)
        
#     # plt.show()
        
#     csv_name = base_path + "_event_stats.csv"
#     create_csv(event_stats, csv_name)
    
#     # average event displays
#     average_speed = np.array(all_event_speeds).mean(axis=0)
#     average_name = base_path + '_event_average'
#     avg_fig, ax = plt.subplots()
#     figs.append(avg_fig)
#     plt.title('Average event speed')
#     display.two_plots(avg_fig, ax, norm_event_time, average_speed, event_stim, average_name, 'Time (s)', 'Mouse Velocity (pix/s)', 'stim (on/off)')
    
#     plt.close()
    
#     save_report(figs, base_path)
            
            

