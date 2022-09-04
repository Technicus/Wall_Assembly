#!/usr/bin/env python3
# version beta

"""
American Softwood Lumber Standard Generator

name: BoardConstructor.py
by:   Technicus
date: September 1st 2022

desc: This python/cadquery code is a component of the larger architectural development concept, "ProjectDesignBuilder".

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

from Calculations.UnitConversion import unit_conversion


def board_cut(board_name_prefix = 'board', board_profile = '2x4', board_length = (114.5, 'in'), units = 'mm', board_count = 1):
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
        (🗸) Add parameters to create multiple boards with single call to function
        (🗸) Add unit conversion
        (☐) Add parameters for placement: position, rotation, angle, etc.
        (☐) Distribute multiple boards
        (☐) Add extension to modify ends with compound miter cuts
        (☐) Add extension to modify profiles
        (☐) Add extension to add notches, holes, or arbitrary cut outs
        (☐) Add export/view option
        (☐) Make path for 'material_profiles_lumber_boards.csv' dynamic
        (☐) Implement error checking
        (☐) Add tests
        (☐) Output log data
        (☐) Reimplement as a class
        (☐) Possibly add more lumber profiles to csv data
        (☐) Add parameter for color
            ! AttributeError: 'Workplane' object has no attribute 'Color'
        (☐) Refine documentation
    """

    board_sketch = []
    boards = []
    board_names = []
    board_obj = None

    with open('./Boards/material_profiles_lumber_boards.csv') as lumber_profiles:
            lumber_profile = reader(lumber_profiles, delimiter=';')
            for row in lumber_profile:
                if row:
                    if row[0] == board_profile:
                        board_profile = []
                        count = 0
                        for col in row:
                            board_profile.append(row[count])
                            count += 1
                        #print(f'  board_profile:\n    {board_profile}\n')

    # Unit conversion
    #unit_conversion(length = float(0), in_units = None, out_units = None)
    board_length = unit_conversion(board_length[0], board_length[1], units)
    board_profile[1], board_profile[4] = unit_conversion(float(board_profile[1]), board_profile[4], units)
    board_profile[2], board_profile[4] = unit_conversion(float(board_profile[2]), board_profile[4], units)
    board_profile[3], board_profile[4] = unit_conversion(float(board_profile[3]), board_profile[4], units)
    #board_profile[4] = 'mm'

    for count in range(int(board_count)):
        #print(f'{count}')
        board_sketch.append(Sketch())
        board_sketch[count] = (
            Sketch()
            .rect(board_profile[1], board_profile[2])
            .vertices()
            .fillet(board_profile[3])
        )

        boards.append(Workplane())
        boards[count] = (
            Workplane()
            .placeSketch(board_sketch[count])
            .extrude(board_length[0])
        )

        board_names.append('')
        board_names[count] = board_name_prefix + '_' + str(count)
        #print(f'{str(board_names[count])}')

    return (boards, board_names, board_profile, board_length)
