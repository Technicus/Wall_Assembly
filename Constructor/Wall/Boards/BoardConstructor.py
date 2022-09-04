#!/usr/bin/env python3
# version beta

"""
American Softwood Lumber Standard Generator

name: BoardConstructor.py
by:   Technicus
date: September 3st 2022

desc: This python/cadquery code is a component of the larger architectural design project "ProjectDesignBuilder".

license:
    Copyright 2022 Technicus

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""


from csv import reader
from cadquery import Sketch, Workplane, exporters, Assembly, Color


def board_cut(board_name = 'board', board_profile = '2x4', board_length = (114.5, 'in'), units = 'mm'):
    """
    Cut Dimenstional Lumber Generator

    Function for creating lengths of dimensional lumber at given length.

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
        Add parameters for placement: position, rotation, angle, etc.
        Add extension to modify ends with compound miter cuts
        Add extension to modify profiles
        Add extension to add notches, holes, or arbitrary cut outs
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

print(f"\n[BoardConstructor]\n\t{board[1]}: {board[2]}\n")

if "show_object" in locals():
    show_object(board[0], board[1])
