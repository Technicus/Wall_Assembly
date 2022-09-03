#!/usr/bin/env python3
# version beta

# example:
# clear; ./WallConstructor.py --length 8ft --height 120.5in --stud_spacing 16in --stud_profile 2x4 --bottom_plate_profile 2x6 --top_plate_profile 2x4
# clear; ./WallConstructor.py --length 10ft --height 90.5in --stud_spacing 24in --stud_profile 2x4 --bottom_plate_profile 2x6 --top_plate_profile 2x4


from cadquery import exporters, Sketch, Workplane, Assembly, Color
import cq_warehouse.extensions
from cq_warehouse.drafting import Draft
from WallParameters import parse_arguments, parameter_check, validate_wall_parameters, unit_conversion
from WallMaterials import board_profile
from WallExports import wall_segment_export, export_evaluation

from math import floor
from sys import exit, argv, stderr #, stdout
from pprint import pprint
#import sys, os, subprocess, string
from subprocess import call
from pathlib import Path
from os import listdir, scandir


def wall_segment_construct(wall_parameters = None):

    # Set wall dimentions, material lengths, number of studs.
    # todo: include parameters for openings, corners and additional features.

    wall_parameters.stud_count = floor(wall_parameters.length / wall_parameters.stud_spacing) + 1

    wall_parameters.studs = []
    for x in range(int(wall_parameters.stud_count)):
        wall_parameters.studs.append("stud_" + str(x))

    print("Studs:")
    print("stud count: {}".format(wall_parameters.stud_count))

    wall_parameters.board_length["studs"] = wall_parameters.height - board_profile(wall_parameters.top_plate_profile)["width"] - board_profile(wall_parameters.bottom_plate_profile)["width"]
    wall_parameters.board_length["top_plate"] = wall_parameters.length
    wall_parameters.board_length["bottom_plate"] = wall_parameters.length

    print(wall_parameters.studs)
    print()
    print("stud_profile ({})".format(wall_parameters.stud_profile))
    print("width:  {}".format(board_profile(wall_parameters.stud_profile)["width"]))
    print("depth:  {}".format(board_profile(wall_parameters.stud_profile)["depth"]))
    print("radius: {} ".format(board_profile(wall_parameters.stud_profile)["radius"]))
    print("stud_length: {}".format(wall_parameters.board_length["studs"]))

    print()
    print("top_plate_profile ({})".format(wall_parameters.top_plate_profile))
    print("width:  {}".format(board_profile(wall_parameters.top_plate_profile)["width"]))
    print("depth:  {}".format(board_profile(wall_parameters.top_plate_profile)["depth"]))
    print("radius: {} ".format(board_profile(wall_parameters.top_plate_profile)["radius"]))
    print("top_plate_length: {}".format(wall_parameters.board_length["top_plate"]))

    print()
    print("bottom_plate_profile ({})".format(wall_parameters.bottom_plate_profile))
    print("width:  {}".format(board_profile(wall_parameters.bottom_plate_profile)["width"]))
    print("depth:  {}".format(board_profile(wall_parameters.bottom_plate_profile)["depth"]))
    print("radius: {} ".format(board_profile(wall_parameters.bottom_plate_profile)["radius"]))
    print("bottom_plate_length: {}".format(wall_parameters.board_length["bottom_plate"]))
    print()

    # Next, create a sketch on a plane with selected board profiles and extrude for each stud, top plate, and bottomplate.
    # A utility/constructor/assistant function of some kind need to be created to help with this.
    # The extra step is necessary because the length of studs is less than the total wall height.
    # Since the wall height is a sum of bottom plate, stud, and top plate.
    # So the stud length needs to be wall height - top plate - bottom plate.
    # For the intial development the given parameters for studs and top plate are 2x4 and bottom plate is 2x6,
    # but this must become dynamic to accept variable paramater inputs for different board profiles.

    # Create board sketch profiles.
    board_stud_profile = (
        Sketch()
        .rect(board_profile(wall_parameters.stud_profile)["width"], board_profile(wall_parameters.stud_profile)["depth"])
        .vertices()
        .fillet(board_profile(wall_parameters.stud_profile)["radius"])
    )
    board_top_plate_profile = (
        Sketch()
        .rect(board_profile(wall_parameters.top_plate_profile)["width"], board_profile(wall_parameters.top_plate_profile)["depth"])
        .vertices()
        .fillet(board_profile(wall_parameters.top_plate_profile)["radius"])
    )
    board_bottom_plate_profile = (
        Sketch()
        .rect(board_profile(wall_parameters.bottom_plate_profile)["width"], board_profile(wall_parameters.bottom_plate_profile)["depth"])
        .vertices()
        .fillet(board_profile(wall_parameters.bottom_plate_profile)["radius"])
    )

    # Create the boards and match them to length for wall.
    board_wall_stud = (
        Workplane()
        .placeSketch(board_stud_profile)
        #.extrude(2984.7)
        .extrude(wall_parameters.board_length["studs"])
        #.extrude(board_profile(wall_parameters.height - board_profile(wall_parameters.top_plate_profile)["width"] - board_profile(wall_parameters.bottom_plate_profile)["width"]))
    )
    board_top_plate = (
        Workplane()
        .placeSketch(board_top_plate_profile)
        #.extrude(2438.4)
        .extrude(wall_parameters.board_length["top_plate"])
        #.extrude(board_profile(wall_parameters.length))
    )

    board_bottom_plate = (
        Workplane()
        .placeSketch(board_bottom_plate_profile)
        #.extrude(2438.4)
        .extrude(wall_parameters.board_length["bottom_plate"])
        #.extrude(board_profile(wall_parameters.length))
    )

    # Create the wall assembly.
    wall = (
        Assembly()
    )

    board_bottom_plate = board_bottom_plate.rotate((0,0,0), (0,1,0), 90)
    board_top_plate = board_top_plate.rotate((0,0,0), (0,1,0), 90)

    wall = (
        Assembly()
        .add(board_bottom_plate,
        #loc=Location(Vector(0, 0, 0), Vector(0, 1, 0), 90),
        name = "board_bottom_plate",
        color = Color("green"))
    )

    wall.add(
        board_top_plate,
        name = "board_top_plate",
        color = Color("brown"))

    for stud in wall_parameters.studs:
        wall.add(
            board_wall_stud,
            name = stud,
            color = Color("brown"))

    for stud in wall_parameters.studs:
        wall.constrain(stud, "FixedRotation", (0, 0, 0))

    for stud in wall_parameters.studs:
        wall.constrain(f"{stud}@faces@<Z", "board_bottom_plate@faces@>Z", "PointInPlane")
        wall.constrain("board_bottom_plate@faces@>Y", f"{stud}@faces@>Y", "PointInPlane", 0)

    wall.constrain(f"{wall_parameters.studs[0]}@faces@<X", "board_bottom_plate@faces@<X", "PointInPlane")
    wall.constrain(f"{wall_parameters.studs[-1]}@faces@>X", "board_bottom_plate@faces@>X", "PointInPlane")

    for stud in range(len(wall_parameters.studs[1:])):
        stud_spacing = wall_parameters.stud_spacing * stud
        wall.constrain("board_bottom_plate@faces@<X", f"{wall_parameters.studs[stud]}@faces@<X", "PointInPlane", stud_spacing)

    wall.constrain("board_top_plate@faces@<X",f"{wall_parameters.studs[0]}@faces@<X",  "PointInPlane")
    wall.constrain("board_top_plate@faces@>X",f"{wall_parameters.studs[-1]}@faces@>X",  "PointInPlane")
    wall.constrain("board_top_plate@faces@<Z", f"{wall_parameters.studs[0]}@faces@>Z", "PointInPlane")
    wall.constrain("board_top_plate@faces@>Y", f"{wall_parameters.studs[0]}@faces@>Y", "PointInPlane")
    wall.constrain("board_top_plate@faces@<Y", f"{wall_parameters.studs[0]}@faces@<Y", "PointInPlane")

    wall.solve()

    return wall

#def main(interface = 'terminal'):
    #if interface == 'terminal':
    #if interface == 'cq-editor':


# Starting from terminal
if __name__ == "__main__":
    #main('terminal')
    wall_parameters = parse_arguments()
    wall_parameters = parameter_check()
    wall_segment = wall_segment_construct(wall_parameters)
    wall_segment_export(wall_segment)
    #dimension_lines = dimension_wall(wall_segment)
    #wall_segment.rotate((0,0,1),90)


# Opening in cq-editor
if "show_object" in locals():
    #main('cq-editor')
    wall_parameters = parameter_check()
    wall_segment = wall_segment_construct(wall_parameters)
    show_object(wall_segment, "wall_segment")
    print(__name__)
    #dimension_lines = dimension_wall(wall_segment)
    #show_object(dimension_lines, "dimension_lines")
    #show_object(wall_segment.rotate((0,1,0),90), "wall_segment")

