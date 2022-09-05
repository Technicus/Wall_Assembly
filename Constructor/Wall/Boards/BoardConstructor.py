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


def board_cut(board_name_prefix = 'board', board_profile = '2x4', board_length = (114.5, 'in'), units = 'mm', board_count = 1, distribution = (16, 'in')):
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
                - It has been added but needs improvement
        (-) Add parameters for placement: position, rotation, angle, etc.
                - Partially added . . . when multiple boards are created they are evenly spaced apart with the 'distribution' parameter
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

    # Unit conversion
    board_length = unit_conversion(board_length[0], board_length[1], units)
    board_profile[1], board_profile[4] = unit_conversion(float(board_profile[1]), board_profile[4], units)
    board_profile[2], board_profile[4] = unit_conversion(float(board_profile[2]), board_profile[4], units)
    board_profile[3], board_profile[4] = unit_conversion(float(board_profile[3]), board_profile[4], units)

    for count in range(int(board_count)):
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

    # This section of code is to distribute multiple boards when they are created.
    # Currently this section is an undocumented messy tangle of code, and there is probably a much simpler way to do this.
    # This section needs to be dramatically improved!
    # So the code checks if the number of boards being created is even or odd.
    # Then it evenly distributes them along the x axis.
    # If it is an even number the center board positioned at the 0 point along the x axis.
    # If it is an odd number of boards being created, the two center most boards are equadistant the 0 point on the x axis.
    print(f'\nBoardConstructor:')
    for count in range(0, len(boards)):
        print(f'  {boards[count]}')

    if (board_count % 2) == 0:
        center_offset = (distribution[0] / 2,  distribution[1])
        center_translate = center_offset[0]
        print(f'\n   -- center_offset even: {center_offset}')
        print(f'   -- center_translate : {center_translate}')
        print(f'   -- board_count even: {board_count % 2}')
        print(f'   -- distribution: {(distribution[0],  distribution[1])}')

        placement_count_down = (int(board_count) / 2)
        print(f'      placement_count: {int(placement_count_down)}')

        placement = ((((distribution[0]) - (center_translate)) * -1) / 2) + 4
        for count in range(int(placement_count_down) - 1, -1, -1):
            print(f'         count: {count}, translate: {center_translate}, placement: {placement - center_translate}')
            boards[count] = boards[count].translate((placement - center_translate, 0))
            placement = (placement + int(distribution[0]) * -1)

        placement = ((distribution[0]) + (center_translate / 2)) - 4
        for count in range(int(placement_count_down), int(board_count), 1):
            print(f'         count: {count}, translate: {center_translate}, placement: {placement - center_translate}')
            boards[count] = boards[count].translate((placement - center_translate, 0))
            placement = (placement + int(distribution[0]))

    else:
        center_offset = (distribution[0],  distribution[1])
        print(f'\n   -- center_offset odd: {center_offset}')
        print(f'   -- board_count odd: {board_count % 2}')
        placement_count_down = (int(board_count) / 2)
        print(f'      placement_count: {int(placement_count_down)}')

        placement = distribution[0] * -1
        for count in range(int(placement_count_down) - 1, -1, -1):
            print(f'         count: {count}, translate: {center_offset}, placement: {placement}')
            boards[count] = boards[count].translate((placement, 0))
            placement = placement + int(distribution[0]) * -1

        print(f'      center_count: {int(placement_count_down)}, translate: 0')
        boards[int(placement_count_down)] = boards[int(placement_count_down)].translate((0, 0))

        placement = distribution[0]
        for count in range(int(placement_count_down) + 1 , int(board_count), 1):
            print(f'         count: {count}, translate: {center_offset}, placement: {placement}')
            boards[count] = boards[count].translate((placement, 0))
            placement = placement + int(distribution[0])

    return (boards, board_names, board_profile, board_length)
