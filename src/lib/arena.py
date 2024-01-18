def get_exit_roi(dimensions):

    roi = [dimensions["arena_left"]-dimensions["exit_left"],
           dimensions["arena_left"]+dimensions["exit_right"],
           dimensions["arena_top"]-dimensions["exit_top"],
           dimensions["arena_top"]+dimensions["exit_bottom"]]
    
    return roi

def get_arena_offset(exit_loc, exit_std):
    
    offset = ((exit_loc[0]-exit_std[0]),(exit_loc[1]-exit_std[1]))
    
    return offset



# def get_exit_loc(filename):
    
#     with open(filename, 'r') as file:
        
#         csvreader = csv.reader(file)
#         for row in csvreader:
#             exit_loc = (int(row[0]), int(row[1]))
            
#     return exit_loc

# def create_exit_roi(size, loc):
    
#     roi_imbalance = settings["roi_imbalance"]
    
#     roi = [int(loc[0] - (size[0]*roi_imbalance)),
#            int(loc[0] + (size[0]*(1-roi_imbalance))),
#            int(loc[1] - (size[1]*0.5)),
#            int(loc[1] + (size[1]*0.5))]