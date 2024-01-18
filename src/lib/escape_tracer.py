import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from . import display, sound, arena, analysing
from .utils import *

class EscapeTracer():
    def __init__(self, tracking_file, settings, dimensions):
        
        for k, v in settings.items():
            setattr(self, k, v)
     
        self.tracking_file = tracking_file
        self.tracking_db = read_tracking_file(self.tracking_file)    
        # time and event attributes
        self.num_frames = self.tracking_db.shape[0]
        frame_time = (1./self.fps)
        self.total_time = self.num_frames * frame_time
        self.time = np.arange(self.num_frames) * frame_time
        self.schedule = (self.t_minus, self.event_length, self.t_plus)
        self.norm_event_time = np.arange(-self.t_minus, (self.event_length+self.t_plus), frame_time) #############
        self.exit_roi = arena.get_exit_roi(dimensions)
        
        # read tracking data
        scorer = self.tracking_db.columns.get_level_values(0)[0]
        self.tracking = self.tracking_db[scorer][self.target_bodypart]
        self.detections = self.tracking['likelihood'].values > self.pcutoff
        self.tracking_detected = self.tracking[self.detections]
    
        # create output folder
        self.assign_analysis_folder()
        self.results_folder = create_folder(self.analysis_folder, "et_output")
        self.base_path = os.path.join(self.results_folder, self.base_name)
        
        # initialise figures list
        self.figs = []
        
    def load_stim_file(self, stim_file):
        
        self.stim_file = stim_file
        
        # read sound data
        if self.stim_file is not None:
            self.sound_data, self.folder, self.base_name = sound.read_sound_file(self.stim_file, self.num_frames)
            self.sound_event_frames = sound.get_sound_events(self.sound_data)
            
    def load_background_image(self, image_file):
        
        self.image_file = image_file

    def assign_analysis_folder(self):
    
        parent_folder = os.path.dirname(self.folder)
        self.analysis_folder = os.path.join(parent_folder, "analysis")
        
        try: 
            os.mkdir(self.analysis_folder)
        except:
            pass
    
    def calc_speeds(self):
        
        self.speeds, self.locs = analysing.calculate_speeds(self.tracking, 
                                                  self.detections, 
                                                  self.num_frames, 
                                                  self.fps, 
                                                  self.base_path, 
                                                  self.exit_roi)

    def global_displays(self, show=False):
        
        # trip grid
        display.trip_grid(self.tracking_detected)
        trip_fig = plt.gcf()
        self.figs.append(trip_fig)
        
        # time plot
        time_fig, ax = plt.subplots()
        self.figs.append(time_fig)
        plt.title('Activity over time')
        
        display.time_plot_on_image(ax, 
                                   self.tracking,
                                   self.fps,
                                   self.pcutoff,
                                   image_file=self.image_file,
                                   length=self.total_time,
                                   show=show)
     
        # speed plot
        speed_fig, speed_ax = plt.subplots()
        self.figs.append(speed_fig)
        plt.title('Velocity')
        
        display.two_plots(speed_fig, 
                          speed_ax, 
                          self.time, 
                          self.speeds, 
                          self.sound_data,
                          x_label='Time (s)', 
                          data1_label='Mouse Velocity (pix/s)', 
                          data2_label='Sound (on/off)',
                          show=show)   
        
    def event_displays(self, show=False):
        
        if self.stim_file is not None:
        
            all_event_speeds = []
            event_stats = []

            for i, event_t0 in enumerate(self.sound_event_frames, 1):
                
                start = event_t0 - (self.t_minus*self.fps)
                sound_end = event_t0 + (self.event_length*self.fps)
                end = sound_end + (self.t_plus*self.fps)
                
                if end < (self.num_frames - (self.t_plus*self.fps)):
                    
                    event_name = 'event_' + str(i)
                    event_folder_name = create_folder(self.results_folder, event_name, append_date=False)
                    event_base_path = os.path.join(event_folder_name, self.base_name + "_" + event_name)
                
                    event_speeds = self.speeds[start:end]
                    event_locs = self.locs[start:end]
                    event_sound = self.sound_data[start:end]
                    event_tracking = self.tracking.loc[start:end]
                    post_sound_speeds = self.speeds[event_t0:end]
                
                    event_speed_df = pd.DataFrame((event_speeds, event_locs))
                    event_speed_df.to_csv(event_base_path + '_speeds.csv')
                    
                    escape_time, max_speed = analysing.find_escape_stats(post_sound_speeds, self.fps)
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
                                show=show)
                    
                    display.two_plots(event_fig, 
                                    speed_ax, 
                                    self.norm_event_time, 
                                    event_speeds, 
                                    event_sound,
                                    x_label='Time (s)', 
                                    data1_label='Mouse Velocity (pix/s)', 
                                    data2_label='Sound (on/off)',
                                    show=show)
                    
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
                            event_sound,
                            x_label='Time (s)', 
                            data1_label='Mouse Velocity (pix/s)', 
                            data2_label='Sound (on/off)',
                            show=show)
            
            plt.close()
            
        else:
            print("Cannot make escape analysis as no stimulus file loaded")
        
    def make_pdf_report(self):
    
        save_report(self.figs, self.base_path)

    
    
    
    
# def analyse(tracking_file, sound_file, exit_file):
    
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
    
#     # read sound data
#     sound, source_dir, base_name = read_sound_file(sound_file, num_frames)
#     sound_event_frames = get_sound_events(sound)
    
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
#     display.two_plots(speed_fig, ax, time, speeds, sound, base_path, 'Time (s)', 'Mouse Velocity (pix/s)', 'Sound (on/off)')

#     # event displays
#     all_event_speeds = []
#     event_stats = []
#     figs.append(trip_fig)
#     figs.append(time_fig)
    
#     for i, event_t0 in enumerate(sound_event_frames, 1):
        
#         start = event_t0 - (t_minus*fps)
#         sound_end = event_t0 + (event_length*fps)
#         end = sound_end + (t_plus*fps)
        
#         if end < (num_frames - (t_plus*fps)):
            
#             event_name = 'event_' + str(i)
#             event_folder_name = create_folder(results_folder, event_name, append_date=False)
#             event_base_path = os.path.join(event_folder_name, base_name + "_" + event_name)
        
#             event_time = time[start:end]
#             event_speeds = speeds[start:end]
#             event_sound = sound[start:end]
#             event_tracking = tracking.loc[start:end]
#             sound_on_speeds = speeds[event_t0:end]
        
#             event_speed_df = pd.DataFrame(event_speeds)
#             event_speed_df.to_csv(event_base_path + '_speeds.csv')
            
#             escape_time, max_speed = find_escape_stats(sound_on_speeds, fps)
#             event_stats.append([i, escape_time, max_speed])
#             event_fig, (ax1, ax2) = plt.subplots(1, 2)
#             figs.append(event_fig)
#             plt.title('Event #' + str(i))
#             display.time_plot_on_image(ax2, event_tracking, event_base_path, fps, pcutoff, schedule=schedule, offset=offset)
#             display.two_plots(event_fig, ax1, norm_event_time, event_speeds, event_sound, event_base_path, 'Time (s)', 'Mouse Velocity (pix/s)', 'Sound (on/off)') 
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
#     display.two_plots(avg_fig, ax, norm_event_time, average_speed, event_sound, average_name, 'Time (s)', 'Mouse Velocity (pix/s)', 'Sound (on/off)')
    
#     plt.close()
    
#     save_report(figs, base_path)
            
            

