#!/usr/bin/env python3
# version beta

# Material data

import csv
from cadquery import Sketch, Workplane


class Board:
    """American Softwood Lumber Standard Generator

    Base Class used to create lengths of dimensional lumber
    Args:
        name (str): given name for board
        profile (str): board profile - e.g. "2x4", the profile is read from the CSV file which brings in depth and width information
        length (tup): the length the board is to be given in a tuple as length and unit of measure ment

    Raises:
        None

    """

    def __init__(self, name: str, profile: str, length: tuple):
        self.name = name
        self.profile = profile
        self.length = length
        self.sketch = Sketch()
        self.workplane = Workplane()


    def profile_set(self):
        """
        Read the materials csv file and find the dimensions for given board profile
        """

        if self.profile == None:
            return None

        with open('./material_profiles_lumber_boards.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            for row in csv_reader:
                if row:
                    if row[0] == self.profile:
                        return (row[0], float(row[1]), float(row[2]), float(row[3]), row[4])


    def build_sketch(self):
        """
        Create board sketch profiles with the dimensions found in material csv file.
        Then place it on the workpland and extrude it the given length.

        TODO:
            Add placement for workplane origin as optional arguments.
        """

        self.sketch().rect(self.profile_set(self)[1], self.profile_set(self)[2]).vertices().fillet(self.profile_set(self)[3])
        self.workplane().placeSketch(self.sketch).extrude(self.length)


    def show_board(self):
        """
        There is a problem here.

        [2022-09-03 22:19:28.516390] ERROR: CQ-Editor: Uncaught exception occurred
            Traceback (most recent call last):
            File "~/miniforge/envs/cadquery/lib/python3.10/site-packages/cq_editor/widgets/object_tree.py", line 250, in addObjects
                ais,shape_display = make_AIS(obj.shape,obj.options)
            File "~/miniforge/envs/cadquery/lib/python3.10/site-packages/cq_editor/cq_utils.py", line 64, in make_AIS
                shape = to_compound(obj)
            File "~/miniforge/envs/cadquery/lib/python3.10/site-packages/cq_editor/cq_utils.py", line 42, in to_compound
                raise ValueError(f'Invalid type {type(obj)}')
            ValueError: Invalid type <class 'temp.Board'>

        """
        show_object(self, "board_stud")


print(f"\nBoard:")

board = Board('stud_00', '2x4', (114.5, 'in'))
print(f"\tname:\t(\'{board.name}\')")
print(f"\tprofile:{board.profile_set()}")
print(f"\tlength:\t{board.length[0]}{board.length[1]}")
print(f"")

# Opening in cq-editor
if "show_object" in locals():
    board.show_board()


