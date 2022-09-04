#!/usr/bin/env python3
# version beta

# Material data

from csv import reader
from cadquery import Sketch, Workplane, exporters, Assembly, Color


def board_cut(board_name = 'board', board_profile = '2x4', board_length = (114.5, 'in'), units = 'mm'):
    """American Softwood Lumber Standard Generator

    Base Class used to create lengths of dimensional lumber
    Args:
        name (str): given name for board
        profile (str): board profile - e.g. "2x4", the profile is read from the CSV file which brings in depth and width information
        length (tup): the length the board is to be given in a tuple as length and unit of measure ment

    Raises:
        None

    Returns:
        tuple of Workplane object representing extruded board of selected profile, board name, and board profile data.

    TODO:
        Reimplement as a class
        Add unit conversion
        Implement error checking
        Add tests
        Output log data
        Possibly add more lumber profiles to csv data
        Add parameter for color
        Add parameter for placement
        Add parameter for position
        Add parameter for rotation
        Add parameter for angle
    """

    board_sketch = Sketch()
    board_workplane = Workplane()
    board_obj = None

    with open('./material_profiles_lumber_boards.csv') as lumber_profiles:
            lumber_profile = reader(lumber_profiles, delimiter=';')
            for row in lumber_profile:
                if row:
                    if row[0] == board_profile:
                        #return (row[0], float(row[1]), float(row[2]), float(row[3]), row[4])
                        board_profile = (row[0], float(row[1]), float(row[2]), float(row[3]), row[4])

    board_sketch = (
        Sketch()
        .rect(board_profile[1], board_profile[2])
        .vertices()
        .fillet(board_profile[3])
    )

    board = (
        Workplane()
        .placeSketch(board_sketch)
        .extrude(board_length[0])
    )

    return (board, board_name, board_profile)

board = board_cut('stud_00', '2x4', (114.5, 'in'))
print(f"\n[BoardConstructor]\n\tprofile: {board[2]}\n")
if "show_object" in locals():
    show_object(board[0], board[1])













# Failed attempt to create a board class.
#class Board:
    #"""American Softwood Lumber Standard Generator

    #Base Class used to create lengths of dimensional lumber
    #Args:
        #name (str): given name for board
        #profile (str): board profile - e.g. "2x4", the profile is read from the CSV file which brings in depth and width information
        #length (tup): the length the board is to be given in a tuple as length and unit of measure ment

    #Raises:
        #None

    #"""

    #def __init__(self, name: str, profile: str, length: tuple):
        #self.name = name
        #self.profile = profile
        #self.length = length
        #self.sketch = Sketch()
        #self.workplane = Workplane()
        #self.obj = object()


    #def profile_set(self):
        #"""
        #Read the materials csv file and find the dimensions for given board profile
        #"""

        #if self.profile == None:
            #return None

        #with open('./material_profiles_lumber_boards.csv') as lumber_profiles:
            #lumber_profile = reader(lumber_profiles, delimiter=';')
            #for row in lumber_profile:
                #if row:
                    #if row[0] == self.profile:
                        #return (row[0], float(row[1]), float(row[2]), float(row[3]), row[4])


    #def cut(self):
        #"""
        #Create board sketch profiles with the dimensions found in material csv file.
        #Then place it on the workpland and extrude it the given length.

        #TODO:
            #Add placement for workplane origin as optional arguments.
        #"""

        #self.sketch().rect(self.profile_set(self)[1], self.profile_set(self)[2]).vertices().fillet(self.profile_set(self)[3])
        #self.obj = self.workplane().placeSketch(self.sketch).extrude(self.length)
        #return self.obj


    ##self.obj = cut(self)

    ##def export(self):
        ###svg_path = "../../Exports/Drawings/svg/"
        ##exporters.export(
            ##self.toCompound(),
            ###svg_path + wall_parameters.name + "_" + file_count(svg_path) + ".svg",
            ##self.name + ".svg",
            ##opt={
                ##"width": 1920,
                ##"height": 1080,
                ##"marginLeft": 10,
                ##"marginTop": 10,
                ###"showAxes": True,
                ##"projectionDir": (0.0, 1, 0.0),
                ###"projectionDir": (1219.200001206249, 140.6877326965332, 1512.0325927734375),
                ##"strokeWidth": 1.0,
                ##"strokeColor": (0, 0, 0),
                ##"hiddenColor": (0, 0, 0),
                ##"showHidden": True,
                ###exporters.ExportTypes.SVG,
            ##},
        ##)


    #def show_board(self):
        #"""
        #There is a problem here.

        #[2022-09-03 22:19:28.516390] ERROR: CQ-Editor: Uncaught exception occurred
            #Traceback (most recent call last):
            #File "~/miniforge/envs/cadquery/lib/python3.10/site-packages/cq_editor/widgets/object_tree.py", line 250, in addObjects
                #ais,shape_display = make_AIS(obj.shape,obj.options)
            #File "~/miniforge/envs/cadquery/lib/python3.10/site-packages/cq_editor/cq_utils.py", line 64, in make_AIS
                #shape = to_compound(obj)
            #File "~/miniforge/envs/cadquery/lib/python3.10/site-packages/cq_editor/cq_utils.py", line 42, in to_compound
                #raise ValueError(f'Invalid type {type(obj)}')
            #ValueError: Invalid type <class 'temp.Board'>

        #"""
        #show_object(self.obj, "board_stud")

##print(f"\tname:\t(\'{board.name}\')")
##print(f"\tprofile:{board.profile_set()}")
##print(f"\tlength:\t{board.length[0]}{board.length[1]}")
##print(f"")

##obj = board.cut()
##board.export()

### Opening in cq-editor
##if "show_object" in locals():
    ###board.show_board()
    ###show_object(obj, "board_stud")
    ##show_object(board, "board_stud")



