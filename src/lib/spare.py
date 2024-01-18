def centres_of_mass(coords):
    
    com_coords = []
    
    for frame_coords in coords:
        
        com = calc_com(frame_coords)
        com_coords.append(com)
        
    return com_coords

def calc_com(frame_coords):
    
    x_values = [x for (x, _) in frame_coords]
    y_values = [y for (_, y) in frame_coords]
    
    x_centre = np.average(x_values)
    y_centre = np.average(y_values)
    
    return (x_centre, y_centre)

def random_walk_plot():
    df = traja.generate(10000)

    hist, image = traja.trip_grid(df, bins=100);

    plt.imshow(hist)
    plt.show()
    
def random_walk_display():
    df = traja.generate(1000)

    anim = traja.animate(df)
    # plot = traja.plot(df)