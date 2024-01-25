def get_exit_roi(dimensions):

    roi = [dimensions["arena"][0]-dimensions["exit"][0],
           dimensions["arena"][0]+dimensions["exit"][1],
           dimensions["arena"][1]-dimensions["exit"][2],
           dimensions["arena"][1]+dimensions["exit"][3]]
    
    return roi

def get_arena_offset(exit_loc, exit_std):
    
    offset = ((exit_loc[0]-exit_std[0]),(exit_loc[1]-exit_std[1]))
    
    return offset