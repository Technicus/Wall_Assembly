#!/usr/bin/env python3
# version beta

# example:
# clear; ./WallConstructor.py --length 8ft --height 120.5in --stud_spacing 16in --stud_profile 2x4 --bottom_plate_profile 2x6 --top_plate_profile 2x4
# clear; ./WallConstructor.py --length 10ft --height 90.5in --stud_spacing 24in --stud_profile 2x4 --bottom_plate_profile 2x6 --top_plate_profile 2x4


from cadquery import exporters, Sketch, Workplane, Assembly, Color
from math import floor
from argparse import ArgumentParser, HelpFormatter, _SubParsersAction, RawTextHelpFormatter, ArgumentError
from sys import exit, argv, stderr #, stdout
from pprint import pprint
from WallParameters import validate_wall_parameters, unit_conversion
#import sys, os, subprocess, string
from subprocess import call
from pathlib import Path
from os import listdir, scandir


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


def export_evaluation(wall = None):

    start = -9
    stop = 10

    x = 0
    y = 0
    z = 0

    count = 0

    for x in range(start, stop, 1):
        for y in range(start, stop, 1):
            for z in range(start, stop, 1):
                count = count + 1
                print('{:04d})'.format(count), end = '')
                if x > -1:
                    print('  {} '.format(x), end = '')
                else:
                    print(' {} '.format(x), end = '')
                if y > -1:
                    print('  {} '.format(y), end = '')
                else:
                    print(' {} '.format(y), end = '')
                if z > -1:
                    print('  {} '.format(z), end = '\n')
                else:
                    print(' {} '.format(z), end = '\n')

                file_export = "../Exports/Drawings/svg/" + str(count).rjust(4,"0")+ "_" + str(x) + "_" + str(y) + "_" + str(z) + "_" + wall_parameters.name + ".svg"
                file_convert = "../Exports/Drawings/png/" + str(count).rjust(4,"0")+ "_" + str(x) + "_" + str(y) + "_" + str(z) + "_" + wall_parameters.name + ".png"
                file_label = str(count).rjust(4,"0")+ "\ " + str(x) + "\ " + str(y) + "\ " + str(z)
                if (x == 0 and y == 0 and z == 0) is False:
                    exporters.export(
                        wall.toCompound(),
                        #"../Exports/Drawings/evaluate/" + str(count).rjust(4,"0")+ "_" + str(x) + "_" + str(y) + "_" + str(z) + "_" + wall_parameters.name + ".svg",
                        file_export,
                        opt={
                            "width": 480,
                            "height": 480,
                            "marginLeft": 10,
                            "marginTop": 10,
                            #"showAxes": True,
                            "projectionDir": (x, y, z),
                            "strokeWidth": 1.0,
                            "strokeColor": (0, 0, 0),
                            "hiddenColor": (0, 0, 0),
                            "showHidden": True,
                            #exporters.ExportTypes.SVG,
                        },
                    )
                    #subprocess.call('convert rgb10.png -pointsize 50 -draw "text 180,180 ' + str(tempo) + '" rgb10-n.png', shell=True)

                    #subprocess.call('convert -density 100 ' + file_export + ' ' + file_convert, shell=True)
                    call('convert -density 100 ' + file_export + ' -background Orange label:' + file_label + ' -gravity Center -append ' + file_convert, shell=True)
                    #-background Orange label:'Faerie Dragon' -gravity Center -append
                    #subprocess.call('convert ' + file_export + ' -background Orange label:' + file_export + ' -gravity Center -append anno_label.jpg')
                else:
                    print("zero fail")
    #subprocess.call("ffmpeg -framerate 30 -pattern_type glob -i '../Exports/Drawings/evaluate/*.png' -c:v libx264 -pix_fmt yuv420p out.mp4")
    #subprocess.call("ffmpeg -framerate 30 -pattern_type glob -i '*.png'-c:v libx264 -vf 'format=yuv444p,scale=480:480' ../Exports/Drawings/mp4/out.mp4")
    #ffmpeg -framerate 30 -pattern_type glob -i '../png/*.png' -c:v libx264 -vf 'format=yuv444p,scale=480:480' ./export_review.mp4





    #exporters.export(wall.toCompound(), "../Exports/Models/" + wall_parameters.name + ".stl", exporters.ExportTypes.STL)
    #exporters.export(wall.toCompound(), "../Exports/Models/" + wall_parameters.name + ".step", exporters.ExportTypes.STEP)

    #exporters.export(wall.toCompound(), "../Exports/Drawings/" + wall_parameters.name + "_00.svg", exporters.ExportTypes.SVG)

    #exporters.export(
        #wall.toCompound(),
        #"../Exports/Drawings/evaluate/" + count + x + y + z + wall_parameters.name + "_test.svg",
        #opt={
            #"width": 1920,
            #"height": 1080,
            #"marginLeft": 10,
            #"marginTop": 10,
            ##"showAxes": True,
            #"projectionDir": (5, -5, 1),
            #"strokeWidth": 1.0,
            #"strokeColor": (0, 0, 0),
            #"hiddenColor": (0, 0, 0),
            #"showHidden": True,
            ##exporters.ExportTypes.SVG,
        #},
    #)


def wall_segment_construct(wall_parameters = None):

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

    #wall_parameters.stud_count = floor(floor(wall_parameters.length / wall_parameters.stud_spacing) + 1)
    wall_parameters.stud_count = floor(wall_parameters.length / wall_parameters.stud_spacing) + 1
    #print(wall_parameters.stud_count)

    #print(floor(wall_parameters.length / wall_parameters.stud_spacing) + 2)
    wall_parameters.studs = []
    for x in range(int(wall_parameters.stud_count)):
        wall_parameters.studs.append("stud_" + str(x))

    print("Studs:")
    print("stud count: {}".format(wall_parameters.stud_count))
    #print("wall height: {}".format(wall_parameters.height))
    #print("top_plate_profile - width: {}".format(board_profile(wall_parameters.top_plate_profile)["width"]))

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

    #export_evaluation(wall)

    ##exporters.export(wall.toCompound(), "../Exports/Models/" + wall_parameters.name + ".stl", exporters.ExportTypes.STL)
    #exporters.export(wall.toCompound(), "../Exports/Models/" + wall_parameters.name + ".step", exporters.ExportTypes.STEP)

    #exporters.export(wall.toCompound(), "../Exports/Drawings/" + wall_parameters.name + "_00.svg", exporters.ExportTypes.SVG)

    #a = self.viewer._get_view()

    #wall.toCompound()
    #wall.rotate((0,0,1),90)

    return wall

#def file_check(file_exam = None):
    #file_to_check = Path(file_exam)

    #if file_to_check.is_file():
        #print(f'The file {file_exam} exists')
        #return file_exam +
    #else:
        #print(f'The file {file_exam} does not exist')
        #return file_exam

def file_count(dir_path = None):
    count = 0
    #dir_path = r'../../'
    for path in scandir(dir_path):
        if path.is_file():
            count += 1
    #print('file count:', count)
    #count = f'{count:02d}'
    return f'{count:02d}'

def wall_segment_export(wall = None):
    svg_path = "../../Exports/Drawings/svg/"
    exporters.export(
        wall.toCompound(),
        svg_path + wall_parameters.name + "_" + file_count(svg_path) + ".svg",
        opt={
            "width": 1920,
            "height": 1080,
            "marginLeft": 10,
            "marginTop": 10,
            #"showAxes": True,
            "projectionDir": (0.0, 1, 0.0),
            #"projectionDir": (1219.200001206249, 140.6877326965332, 1512.0325927734375),
            "strokeWidth": 1.0,
            "strokeColor": (0, 0, 0),
            "hiddenColor": (0, 0, 0),
            "showHidden": True,
            #exporters.ExportTypes.SVG,
        },
    )


def parameter_check():
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

    #wall_segment(wall_parameters)

    with open('../../Exports/Info/' + wall_parameters.name + '.info', 'w') as f:
        f.write("Parameters:\n")
        f.write("> {}\n".format(' '.join(argv)))

    print("---------------".format())
    print("> {}".format(' '.join(argv)))
    print("name: \t{}".format(wall_parameters.name))
    print("{}".format(listdir('../../Exports/Models/')))
    #print("../Exports/Models/{}.stl".format(wall_parameters.name))
    #print("../Exports/Models/{}.step".format(wall_parameters.name))
    print("---------------".format())

    #return wall_segment()
    return wall_parameters


# Starting from terminal
if __name__ == "__main__":
    wall_parameters = parameter_check()
    wall_segment = wall_segment_construct(wall_parameters)
    wall_segment_export(wall_segment)


# Opening in cq-editor
if "show_object" in locals():
    wall_parameters = parameter_check()
    wall_segment = wall_segment_construct(wall_parameters)
    show_object(wall_segment, "wall_segment")

