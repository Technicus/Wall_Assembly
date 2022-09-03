#!/usr/bin/env python3
# version beta


# Test script to evaluate argument processing for converting length units.
# Example:
#clear; ./argtest.py --length 8ft --height 120.5in --stud_spacing 16in --stud_profile 2x4 --bottom_plate_profile 2x6 --top_plate_profile 2x4


# I am trying to program some input validation to check the arguments, but I am not going to complete this now.
#from cadquery import exporters, Sketch, Workplane, Assembly, Color
#from math import floor
from argparse import ArgumentParser, HelpFormatter, _SubParsersAction, RawTextHelpFormatter, ArgumentError
from pprint import pprint
from re import findall, split, finditer

# Set defaults, eventually this value will be populated from a defaults config file.
default_unit = 'Default'
default_length = '0'
default_height = '0'
default_stud_spacing = '0'
default_profile_stud = '2x4'
default_profile_bottom_plate = '2x4'
default_profile_top_plate = '2x4'
default_name = 'wall'

#def parse_arguments(arguments = argv[1:]):
def parse_arguments():
    # Create an argument object
    arguments = ArgumentParser()

    # Define accepted arguments
    arguments.add_argument(
        "--length",
        help="legth of wall",
        type = str,
        default = '8ft',
        nargs = '?'
    )
    arguments.add_argument(
        "length_units",
        help="unit of measurement",
        type = str,
        choices = ['in', 'ft', 'yd', 'mm', 'cm', 'm', 'Default'],
        default = 'in',
        nargs = '?'
    )
    arguments.add_argument(
        "--height",
        help="height of wall",
        type = str,
        default = '120.5in',
        nargs = '?'
    )
    arguments.add_argument(
        "height_units",
        help="unit of measurement",
        type = str,
        choices=['in', 'ft', 'yd', 'mm', 'cm', 'm', 'Default'],
        default = 'in',
        nargs = '?'
    )
    arguments.add_argument(
        "--stud_spacing",
        help="spacing of studs",
        type = str,
        default = '16in',
        nargs = '?'
    )
    arguments.add_argument(
        "stud_spacing_units",
        help="unit of measurement",
        type = str,
        choices = ['in', 'ft', 'yd', 'mm', 'cm', 'm', 'Default'],
        default = 'in',
        nargs = '?'
    )
    arguments.add_argument(
        "--stud_profile",
        help="profile of stud board",
        type = str,
        choices=['1x1', '2x2', '2x3', '2x4', '2x6', '2x8', '2x10', '2x12', '4x4', 'Default'],
        default = '2x4',
        nargs = '?'
    )
    arguments.add_argument(
        "--bottom_plate_profile",
        help="profile of bottom plate board",
        type = str,
        choices=['1x1', '2x4', '2x3', '2x4', '2x6', '2x8', '2x10', '2x12', '4x4', 'Default'],
        default = '2x6'
    )
    arguments.add_argument(
        "--top_plate_profile",
        help="profile of top plate board",
        type = str,
        choices=['1x1', '2x2', '2x3', '2x4', '2x6', '2x8', '2x10', '2x12', '4x4', 'Default'],
        default = '2x4'
    )
    arguments.add_argument(
        "--name",
        help="Provide a name for the wall segment.",
        type = str,
        default = 'wall'
    )
    arguments.add_argument(
        "--format",
        help="Provide export format for the wall segment.",
        type = str,
        default = 'STEP'
    )
    #arguments.add_argument(
        #"--name",
        #help="Provide export filename for the wall segment.",
        #type = str,
        #default = 'default_name'
    #)
    return arguments.parse_args()

# A unit conversion function that accepts an input value, units for that value and the desired conversion unit.
# Input validation should be implemented
def unit_conversion(length = float(0), in_units = None, out_units = None):
    if in_units == 'in':
        if out_units == 'in':
            return length, out_units
        if out_units == 'ft':
            return length / 12, out_units
        if out_units == 'yd':
            return length / 36, out_units
        if out_units == 'mm':
            return length * 25.4, out_units
        if out_units == 'cm':
            return length * 2.54, out_units
        if out_units == 'm':
            return length * 0.0254, out_units
    if in_units == 'ft':
        if out_units == 'in':
            return length * 12, out_units
        if out_units == 'ft':
            return length, out_units
        if out_units == 'yd':
            return length / 3, out_units
        if out_units == 'mm':
            return length * 304.8, out_units
        if out_units == 'cm':
            return length * 30.48, out_units
        if out_units == 'm':
            return length * 0.3048, out_units
    if in_units == 'yd':
        if out_units == 'in':
            return length * 36, out_units
        if out_units == 'ft':
            return length * 3, out_units
        if out_units == 'yd':
            return length, out_units
        if out_units == 'mm':
            return length * 9.144, out_units
        if out_units == 'cm':
            return length * 91.44, out_units
        if out_units == 'm':
            return length * 0.9144, out_units
    if in_units == 'mm':
        if out_units == 'in':
            return length / 25.4, out_units
        if out_units == 'ft':
            return length / 304.8, out_units
        if out_units == 'yd':
            return length /9.144, out_units
        if out_units == 'mm':
            return length, out_units
        if out_units == 'cm':
            return length / 10, out_units
        if out_units == 'm':
            return length / 1000, out_units
    if in_units == 'cm':
        if out_units == 'in':
            return length / 2.54, out_units
        if out_units == 'ft':
            return length / 30.48, out_units
        if out_units == 'yd':
            return length / 91.44, out_units
        if out_units == 'mm':
            return length * 10, out_units
        if out_units == 'cm':
            return length, out_units
        if out_units == 'm':
            return length / 100, out_units
    if in_units == 'm':
        if out_units == 'in':
            return length / 0.0254, out_units
        if out_units == 'ft':
            return length * 3.280839895, out_units
        if out_units == 'yd':
            return length / 0.9144, out_units
        if out_units == 'mm':
            return length * 1000, out_units
        if out_units == 'cm':
            return length * 100, out_units
        if out_units == 'm':
            return length, out_units


# This is a function to destinguish the unit from measurement if they are in a single string.
def parse_units(number_units = None):
    number = 0
    unit = ''

    # This is not quite right.
    # If no number is provided and only unit, first letter of unit is assigned to number.
    REG_STR = r'([a-zA-Z])|(\.\d+)|(\d+\.\d+)|(\d+)'
    matches = [m.group() for m in finditer(REG_STR, number_units) if finditer(REG_STR, number_units)]

    number = matches[0]
    unit = findall(r'[a-zA-Z]', number_units)
    unit = ''.join(unit)

    return number, unit

#if "show_object" not in locals():
    #wall_parameters = arguments.parse_args()
    #wall_parameters = parse_arguments()

#wall_parameters = parse_arguments()


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
#print()

# Check that units are valid
def validate_wall_parameters(wall_parameters = None):
    valid_units = ['in', 'ft', 'yd', 'mm', 'cm', 'm', '\'', '\'\'', '\"', 'Default']
    default_unit = 'mm'
    default_length = '0'
    default_height = '0'
    default_stud_spacing = '0'
    default_profile_stud = '2x4'
    default_profile_bottom_plate = '2x4'
    default_profile_top_plate = '2x4'

    wall_parameters.length_units = parse_units(wall_parameters.length)[1]
    wall_parameters.length = parse_units(wall_parameters.length)[0]
    wall_parameters.height_units = parse_units(wall_parameters.height)[1]
    wall_parameters.height = parse_units(wall_parameters.height)[0]
    wall_parameters.stud_spacing_units = parse_units(wall_parameters.stud_spacing)[1]
    wall_parameters.stud_spacing = parse_units(wall_parameters.stud_spacing)[0]
    wall_parameters.board_length = {}

    if "show_object" in locals():
        #parameter_check()
        #--length 8ft --height 120.5in --stud_spacing 16in --stud_profile 2x4 --bottom_plate_profile 2x6 --top_plate_profile 2x4
        wall_parameters.length_units = 'ft'
        wall_parameters.length = '8'
        wall_parameters.height_units = 'in'
        wall_parameters.height = '120.5'
        wall_parameters.stud_spacing_units = 'in'
        wall_parameters.stud_spacing = '16'
        wall_parameters.board_length = {}

    #if "show_object" in locals():
        ##parameter_check()default_height
        ##--length 8ft --height 120.5in --stud_spacing 16in --stud_profile 2x4 --bottom_plate_profile 2x6 --top_plate_profile 2x4
        #parse_units(wall_parameters.length)[1] = 'ft'
        #parse_units(wall_parameters.length)[0] = '8'
        #parse_units(wall_parameters.height)[1] = 'in'
        #parse_units(wall_parameters.height)[0] = '120.5'
        #parse_units(wall_parameters.stud_spacing)[1] = 'in'
        #parse_units(wall_parameters.stud_spacing)[0] = '16'

    #print(parse_units(wall_parameters.length)[0])
    #print(parse_units(wall_parameters.length)[1])
    #print(parse_units(wall_parameters.height)[0])
    #print(parse_units(wall_parameters.height)[1])
    #print(parse_units(wall_parameters.stud_spacing)[0])
    #print(parse_units(wall_parameters.stud_spacing)[1])
    #print()

    if wall_parameters.length == None:
        wall_parameters.length = default_length

    #print("length: \t\t{}".format(wall_parameters.length))
    #print("length_units: \t\t{}".format(wall_parameters.length_units))
    #print("height: \t\t{}".format(wall_parameters.height))
    #print("height_units: \t\t{}".format(wall_parameters.height_units))
    #print("stud_spacing: \t\t{}".format(wall_parameters.stud_spacing))
    #print("stud_spacing_units: \t{}".format(wall_parameters.stud_spacing_units))
    #print("stud_profile: \t\t{}".format(wall_parameters.stud_profile))
    #print("bottom_plate_profile: \t{}".format(wall_parameters.bottom_plate_profile))
    #print("top_plate_profile: \t{}".format(wall_parameters.top_plate_profile))

    return wall_parameters

    #print(wall_parameters.length)
    #print(wall_parameters.length_units)
    #print()
    #print(parse_units(wall_parameters.length)[0])
    #print(parse_units(wall_parameters.length)[1])

    #if wall_parameters.length_units == None:
        ##wall_parameters.length_units = "UNITS_UNKOWN" parse_units(wall_parameters.length)[1]
        #print("Argument \'length_units\' ignored, attempting to assign unit.")
        #wall_parameters.length_units = parse_units(wall_parameters.length)[1]
        #print("\t 'length_units\' assigned to: {}".format(wall_parameters.length_units))
    #if wall_parameters.length_units != None:
        ##wall_parameters.length_units = "UNITS_UNKOWN" parse_units(wall_parameters.length)[1]
        #print("Argument \'length_units\' provided, attempting to validate unit.")
        #if parse_units(wall_parameters.length)[1] != wall_parameters.length_units:
            #print("Conflicting units: ({})({}), please resolve the unit assignment".format(parse_units(wall_parameters.length)[1], wall_parameters.length_units))
        #print("\t 'length_units\' assigned to: {}".format(wall_parameters.length_units))
    #if wall_parameters.height_units == None:
        #print("Argument \'height_units\' ignored, attempting to assign unit.")
        #wall_parameters.height_units = parse_units(wall_parameters.height_units)[1]
        #print("\t 'length_units\' assigned to: {}".format(wall_parameters.length_units))
        ##wall_parameters.height_units = "UNITS_UNKOWN" parse_units(wall_parameters.height)[1]
    #if wall_parameters.stud_spacing_units == None:
        #print("Argument \'stud_spacing_units\' ignored, attempting to assign unit.")
        #wall_parameters.stud_spacing_units = parse_units(wall_parameters.stud_spacing_units)[1]
        #print("\t 'stud_spacing_units\' assigned to: {}".format(wall_parameters.stud_spacing_units))
        ##wall_parameters.stud_spacing_units = "UNITS_UNKOWN" parse_units(wall_parameters.stud_spacing_units)[1]
    #if wall_parameters.stud_spacing_units == None:
        #wall_parameters.stud_spacing_units = "UNITS_UNKOWN"
    #print(parse_units(wall_parameters.length)[1])
    #print()




##pprint(vars(args))
#print("length: \t\t{}".format(wall_parameters.length))
#print("length_units: \t\t{}".format(wall_parameters.length_units))
#print("height: \t\t{}".format(wall_parameters.height))
#print("height_units: \t\t{}".format(wall_parameters.height_units))
#print("stud_spacing: \t\t{}".format(wall_parameters.stud_spacing))
#print("stud_spacing_units: \t{}".format(wall_parameters.stud_spacing_units))
#print("stud_profile: \t\t{}".format(wall_parameters.stud_profile))
#print("bottom_plate_profile: \t{}".format(wall_parameters.bottom_plate_profile))
#print("top_plate_profile: \t{}".format(wall_parameters.top_plate_profile))
#print()
#validate_parse_units()
#print()

#print(parse_units(wall_parameters.length)[0])
#print(parse_units(wall_parameters.length)[1])
#print(parse_units(wall_parameters.height))
#print(parse_units(wall_parameters.stud_spacing))

#wall_parameters.length = unit_conversion(float(parse_units(wall_parameters.length)[0]), parse_units(wall_parameters.length)[1], 'mm')
#wall_parameters.length_units = 'mm'

#wall_parameters.height = unit_conversion(float(parse_units(wall_parameters.height)[0]), parse_units(wall_parameters.height_units)[1], 'mm')
#wall_parameters.height_units = 'mm'

#wall_parameters.stud_spacing = unit_conversion(float(parse_units(wall_parameters.stud_spacing)[0]), parse_units(wall_parameters.stud_spacing_units)[1], 'mm')
#wall_parameters.stud_spacing_units = 'mm'

#pprint(vars(args))


#clear; ./argtest.py --length 8ft --height 120.5in --stud_spacing 16in --stud_profile 2x4 --bottom_plate_profile 2x6 --top_plate_profile 2x4







#def validate_parse_units(args = args):
    #valid_units = ['in', 'ft', 'yd', 'mm', 'cm', 'm', '\'', '\'\'', '\"', 'Default']
    #default_unit = 'mm'
    #default_length = '0'
    #default_height = '0'
    #default_stud_spacing = '0'
    #default_profile_stud = '2x4'
    #default_profile_bottom_plate = '2x4'
    #default_profile_top_plate = '2x4'

    #wall_parameters.length = parse_units(wall_parameters.length)[0]
    #print(parse_units(wall_parameters.length)[1])
    #wall_parameters.length_units = parse_units(wall_parameters.length)[1]
    #wall_parameters.height = parse_units(wall_parameters.height)[0]
    #wall_parameters.height_units = parse_units(wall_parameters.height)[1]
    #wall_parameters.stud_spacing = parse_units(wall_parameters.stud_spacing)[0]
    #wall_parameters.stud_spacing_units = parse_units(wall_parameters.stud_spacing)[1]

    #print("length: \t\t{}".format(wall_parameters.length))
    #print("length_units: \t\t{}".format(wall_parameters.length_units))
    #print("height: \t\t{}".format(wall_parameters.height))
    #print("height_units: \t\t{}".format(wall_parameters.height_units))
    #print("stud_spacing: \t\t{}".format(wall_parameters.stud_spacing))
    #print("stud_spacing_units: \t{}".format(wall_parameters.stud_spacing_units))
    #print("stud_profile: \t\t{}".format(wall_parameters.stud_profile))
    #print("bottom_plate_profile: \t{}".format(wall_parameters.bottom_plate_profile))
    #print("top_plate_profile: \t{}".format(wall_parameters.top_plate_profile))

    ##if wall_parameters.length == None:
        ##wall_parameters.length = default_length

    ##print(wall_parameters.length)
    ##print(wall_parameters.length_units)
    ##print()
    ##print(parse_units(wall_parameters.length)[0])
    ##print(parse_units(wall_parameters.length)[1])

    ##if wall_parameters.length_units == None:
        ###wall_parameters.length_units = "UNITS_UNKOWN" parse_units(wall_parameters.length)[1]
        ##print("Argument \'length_units\' ignored, attempting to assign unit.")
        ##wall_parameters.length_units = parse_units(wall_parameters.length)[1]
        ##print("\t 'length_units\' assigned to: {}".format(wall_parameters.length_units))
    ##if wall_parameters.length_units != None:
        ###wall_parameters.length_units = "UNITS_UNKOWN" parse_units(wall_parameters.length)[1]
        ##print("Argument \'length_units\' provided, attempting to validate unit.")
        ##if parse_units(wall_parameters.length)[1] != wall_parameters.length_units:
            ##print("Conflicting units: ({})({}), please resolve the unit assignment".format(parse_units(wall_parameters.length)[1], wall_parameters.length_units))
        ##print("\t 'length_units\' assigned to: {}".format(wall_parameters.length_units))
    ##if wall_parameters.height_units == None:
        ##print("Argument \'height_units\' ignored, attempting to assign unit.")
        ##wall_parameters.height_units = parse_units(wall_parameters.height_units)[1]
        ##print("\t 'length_units\' assigned to: {}".format(wall_parameters.length_units))
        ###wall_parameters.height_units = "UNITS_UNKOWN" parse_units(wall_parameters.height)[1]
    ##if wall_parameters.stud_spacing_units == None:
        ##print("Argument \'stud_spacing_units\' ignored, attempting to assign unit.")
        ##wall_parameters.stud_spacing_units = parse_units(wall_parameters.stud_spacing_units)[1]
        ##print("\t 'stud_spacing_units\' assigned to: {}".format(wall_parameters.stud_spacing_units))
        ###wall_parameters.stud_spacing_units = "UNITS_UNKOWN" parse_units(wall_parameters.stud_spacing_units)[1]
    ##if wall_parameters.stud_spacing_units == None:
        ##wall_parameters.stud_spacing_units = "UNITS_UNKOWN"
    ##print(parse_units(wall_parameters.length)[1])
    #print()


