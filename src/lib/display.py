import matplotlib.pyplot as plt
import traja
import numpy as np

def get_cmap(n, name='hsv'):
    
    return plt.cm.get_cmap(name, n)

def histogram(vector, color, bins):
    
    dvector = np.diff(vector)
    dvector = dvector[np.isfinite(dvector)]
    plt.hist(dvector,color=color,histtype='step',bins=bins)

def trip_grid(tracking, grid_bins=20, show=False):
    
    hist, image = traja.trip_grid(tracking, bins=grid_bins);
    plt.gca().invert_yaxis()
    
    if show: plt.show()

def time_plot_on_image(ax, tracking, fps, pcutoff, image_file=None, schedule=None, length=None, colormap='jet', offset=(0, 0), show=False):
    ''' Plots poses vs time; pose x vs pose y; histogram of differences and likelihoods.'''
    
    plt.rcParams["figure.figsize"] = [16, 8]
    plt.rcParams["figure.autolayout"] = True
    
    if image_file is not None:
        im = plt.imread(image_file)
        im = ax.imshow(im)
        
    total_time = sum(schedule) if schedule is not None else length
    
    colors = get_cmap(total_time*fps, name = colormap)

    Index = tracking['likelihood'].values > pcutoff
    x = tracking['x'].values[Index] - offset[0]
    y = tracking['y'].values[Index] - offset[1]
    colors = [i/fps for i, x in enumerate(Index) if x]

    plt.scatter(x, y, c=colors, cmap='viridis', s=5, vmin=0, vmax=total_time)   # 'viridis' is one of the available colormaps
    colorbar = plt.colorbar()
    colorbar.set_label('Time (s)')  # Set the label for the colorbar
    
    if schedule is not None:
        light_on_frame = schedule[0]*fps
        plt.scatter(x[light_on_frame],y[light_on_frame],c='red', s=50, marker='x', label='Sound on')

    if show: plt.show()
    
def sound_plot(video_name, length_seconds, averages, n_highs, bin_sound, threshold, save=True, show=False):
    
    fig, axs = plt.subplots(3, 1)
    fig.suptitle('Sound Signal')
    
    axs[0].step(length_seconds, averages)
    axs[0].set_title("Average intensity")
    axs[0].set_ylim(bottom=0, top=120)
    axs[1].step(length_seconds, n_highs)
    axs[1].axhline(y=threshold, color='r', linestyle='-') 
    axs[1].set_title("Bright pixels")
    axs[1].set_ylim(bottom=0, top=120)
    axs[2].step(length_seconds, bin_sound)
    axs[2].set_title("Sound on/off")
    
    base_name = video_name.removesuffix("_signal.avi")
    
    if save: plt.savefig(base_name + '_sound_analysis.jpg', format='jpg')
    
    if show: plt.show()

def two_plots(fig, ax1, x, data1, data2, x_label, data1_label, data2_label, v_lim=800, show=False):
    # Create some mock data
    
    color = 'tab:red'
    ax1.set_xlabel(x_label)
    ax1.set_ylabel(data1_label, color=color)
    ax1.set_ylim(bottom=0, top=v_lim)
    ax1.plot(x, data1, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel(data2_label, color=color)  # we already handled the x-label with ax1
    ax2.set_ylim(bottom=0, top=1.2)
    ax2.plot(x, data2, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    # plt.savefig(base_name + '_speed_plot.jpg', format='jpg')
    
    if show: plt.show()

def dlc_plots(tracking, bodyparts2plot, scorer, dim, base_name, legend=False, alphavalue=.2, pcutoff=.5, colormap='jet'):
    ''' Plots poses vs time; pose x vs pose y; histogram of differences and likelihoods.'''
    colors = get_cmap(len(bodyparts2plot), name = colormap)

    for target_bodypartindex, target_bodypart in enumerate(bodyparts2plot):
        Index=tracking[scorer][target_bodypart]['likelihood'].values > pcutoff
        plt.plot(tracking[scorer][target_bodypart]['x'].values[Index],tracking[scorer][target_bodypart]['y'].values[Index],'.',color=colors(target_bodypartindex),alpha=alphavalue)

    plt.xlim(0, dim[0])
    plt.ylim(0, dim[1])
    
    if legend:
        sm = plt.cm.ScalarMappable(cmap=plt.get_cmap(colormap), norm=plt.Normalize(vmin=0, vmax=len(bodyparts2plot)-1))
        sm._A = []
        cbar = plt.colorbar(sm,ticks=range(len(bodyparts2plot)))
        cbar.set_ticklabels(bodyparts2plot)
    

if __name__ == '__main__':
    
    time_plot_on_image()