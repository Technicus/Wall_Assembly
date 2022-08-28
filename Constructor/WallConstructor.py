#!/usr/bin/env python3
# version beta

# example:
# clear; ./WallConstructor.py --length 8ft --height 120.5in --stud_spacing 16in --stud_profile 2x4 --bottom_plate_profile 2x6 --top_plate_profile 2x4
# clear; ./WallConstructor.py --length 10ft --height 90.5in --stud_spacing 24in --stud_profile 2x4 --bottom_plate_profile 2x6 --top_plate_profile 2x4

from cadquery import exporters, Sketch, Workplane, Assembly, Color
from math import floor
from argparse import ArgumentParser, HelpFormatter, _SubParsersAction, RawTextHelpFormatter, ArgumentError
from sys import exit, argv, stderr #, stdout
from os import listdir
from pprint import pprint
from WallParameters import validate_wall_parameters, unit_conversion

def board_profile(board_dimensions = None):
    if board_dimensions  == '2x4':
        # Set board dimentions for dimentional lumbar in metric
        profile = {
            "width": 38,
            "depth": 89,
            "radius": 3.2
        }
        return profile
    if board_dimensions  == '2x6':
        profile = {
            "width": 38,
            "depth": 140,
            "radius": 3.2
        }
        return profile

def wall_segment(wall_parameters = None):

    # Set wall dimentions, material lengths, number of studs.
    # todo: include parameters for openings, corners and additional features.
    #wall_parameters = {
        ##"length": 2438, # 8',
        ##"height": "117.5in",
        ##"stud_spacing": 406.4, # 16"
        ##"stud": "2X4",
        ##"bottom_plate": "2X6",
        ##"top_plate": "2X4",
        #"stud_length": 2908.3, # 114.5"
        #"bottom_plate_length": 2438, # 8'
        #"top_plate_length": 2438, # 8'
        #"blocking": 0, # bottom_plate_length / stud_spacing round up
        #"studs": [],
        #"openings": [],
        #"sheeting": []
    #}

    wall_parameters.stud_count = floor(floor(wall_parameters.length / wall_parameters.stud_spacing) + 1)
    #print(wall_parameters.stud_count)

    #print(floor(wall_parameters.length / wall_parameters.stud_spacing) + 2)
    wall_parameters.studs = []
    for x in range(int(wall_parameters.stud_count)):
        wall_parameters.studs.append("stud_"+str(x))

    wall_parameters.board_length["studs"] = wall_parameters.height - board_profile(wall_parameters.top_plate_profile)["width"] - board_profile(wall_parameters.bottom_plate_profile)["width"]
    wall_parameters.board_length["top_plate"] = wall_parameters.length
    wall_parameters.board_length["bottom_plate"] = wall_parameters.length

    print("Studs:")
    print(wall_parameters.studs)
    print()
    print("stud_profile ({})".format(wall_parameters.stud_profile))
    print("width:  {}".format(board_profile(wall_parameters.stud_profile)["width"]))
    print("depth:  {}".format(board_profile(wall_parameters.stud_profile)["depth"]))
    print("radius: {} ".format(board_profile(wall_parameters.stud_profile)["radius"]))
    print("stud_length: {}".format(wall_parameters.board_length["studs"]))
    #print("stud_length: {}".format(wall_parameters.height - board_profile(wall_parameters.top_plate_profile)["width"] - board_profile(wall_parameters.bottom_plate_profile)["width"]))

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
    #for x in range(int(wall_parameters["stud_count"])):
        #wall_parameters["studs"].append("stud_"+str(x))

    # Next, create a sketch on a plane with selected board profiles and extrude for each stud, top plate, and bottomplate.
    # A utility/constructor/assistant function of some kind need to be created to help with this.
    # The extra step is necessary because the length of studs is less than the total wall height.
    # Since the wall height is a sum of bottom plate, stud, and top plate.
    # So the stud length needs to be wall height - top plate - bottom plate.
    # For the intial development the given parameters for studs and top plate are 2x4 and bottom plate is 2x6,
    # but this must become dynamic to accept variable paramater inputs for different board profiles.

    ## Set board dimentions for dimentional lumbar in metric
    #board_dimensions_2x4 = {
        #"width": 38,
        #"depth": 89,
        #"radius": 3.2
    #}

    #board_dimensions_2x6 = {
        #"width": 38,
        #"depth": 140,
        #"radius": 3.2
    #}

    # Create board sketch profiles.
    board_stud_profile = (
        Sketch()
        #.rect(board_profile(wall_parameters(stud_profile))["width"], board_profile(wall_parameters(stud_profile))["depth"])
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

    #exporters.export(wall.toCompound(), "../Exports/Models/wall.stl", exporters.ExportTypes.STL)
    exporters.export(wall.toCompound(), "../Exports/Models/" + wall_parameters.name + ".step", exporters.ExportTypes.STEP)
    #exporters.export(wall.toCompound(), "../Exports/Models/wall.step", exporters.ExportTypes.STEP)

    exporters.export(
        wall.toCompound(),
        "../Exports/Drawings/" + wall_parameters.name + ".svg",
        opt={
            "width": 300,
            "height": 300,
            "marginLeft": 10,
            "marginTop": 10,
            "showAxes": False,
            "projectionDir": (0.0, 0.0, 0.5),
            "strokeWidth": 0.25,
            "strokeColor": (255, 0, 0),
            "hiddenColor": (0, 0, 255),
            "showHidden": True,
        },
    )

    if "show_object" in locals():
        show_object(wall, "wall")


# Proceed through the main() entrance.
if __name__ == "__main__":
    wall_parameters = validate_wall_parameters()

    print()
    print("length: \t\t{}".format(wall_parameters.length))
    print("length_units: \t\t{}".format(wall_parameters.length_units))
    print("height: \t\t{}".format(wall_parameters.height))
    print("height_units: \t\t{}".format(wall_parameters.height_units))
    print("stud_spacing: \t\t{}".format(wall_parameters.stud_spacing))
    print("stud_spacing_units: \t{}".format(wall_parameters.stud_spacing_units))
    print("stud_profile: \t\t{}".format(wall_parameters.stud_profile))
    print("bottom_plate_profile: \t{}".format(wall_parameters.bottom_plate_profile))
    print("top_plate_profile: \t{}".format(wall_parameters.top_plate_profile))
    print()

    (wall_parameters.length, wall_parameters.length_units) = unit_conversion(float(wall_parameters.length), wall_parameters.length_units, 'mm')
    (wall_parameters.height, wall_parameters.height_units) = unit_conversion(float(wall_parameters.height), wall_parameters.height_units, 'mm')
    (wall_parameters.stud_spacing, wall_parameters.stud_spacing_units) = unit_conversion(float(wall_parameters.stud_spacing), wall_parameters.stud_spacing_units, 'mm')

    print("length: \t\t{}".format(wall_parameters.length))
    print("length_units: \t\t{}".format(wall_parameters.length_units))
    print("height: \t\t{}".format(wall_parameters.height))
    print("height_units: \t\t{}".format(wall_parameters.height_units))
    print("stud_spacing: \t\t{}".format(wall_parameters.stud_spacing))
    print("stud_spacing_units: \t{}".format(wall_parameters.stud_spacing_units))
    print("stud_profile: \t\t{}".format(wall_parameters.stud_profile))
    print("bottom_plate_profile: \t{}".format(wall_parameters.bottom_plate_profile))
    print("top_plate_profile: \t{}".format(wall_parameters.top_plate_profile))
    print()

    wall_segment(wall_parameters)

    with open('../Exports/Info/' + wall_parameters.name + '.info', 'w') as f:
        f.write("Parameters:\n")
        f.write("> {}\n".format(' '.join(argv)))

    print("---------------".format())
    print("> {}".format(' '.join(argv)))
    print("name: \t{}".format(wall_parameters.name))
    print("{}".format(listdir('../Exports/Models/')))
    #print("../Exports/Models/{}.stl".format(wall_parameters.name))
    #print("../Exports/Models/{}.step".format(wall_parameters.name))
    print("---------------".format())
