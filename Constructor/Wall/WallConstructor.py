#!/usr/bin/env python3
# version beta

# example:
# clear; ./WallConstructor.py --length 8ft --height 120.5in --stud_spacing 16in --stud_profile 2x4 --bottom_plate_profile 2x6 --top_plate_profile 2x4
# clear; ./WallConstructor.py --length 10ft --height 90.5in --stud_spacing 24in --stud_profile 2x4 --bottom_plate_profile 2x6 --top_plate_profile 2x4


from cadquery import exporters, Sketch, Workplane, Assembly, Color
import cq_warehouse.extensions
from cq_warehouse.drafting import Draft
#from WallParameters import parse_arguments, parameter_check, validate_wall_parameters, unit_conversion
#from WallMaterials import board_profile
#from WallExports import wall_segment_export, export_evaluation

from Boards.BoardConstructor import board_cut
from Calculations.UnitConversion import unit_conversion

from math import floor
from sys import exit, argv, stderr #, stdout
from pprint import pprint
#import sys, os, subprocess, string
from subprocess import call
from pathlib import Path
from os import listdir, scandir


def cut_boards():
    return board_cut('stud', '2x4', (114.5, 'in'), board_count = 2, units = 'in')


def report_boards(boards = None):
    # Add data logging process here
    print(f"\n|BoardConstructor|\n  Boards:\n    {boards[1]}\n  Profile:\n    {boards[2]}\n  Length:\n    {boards[3]}\n")


# Starting from terminal
if __name__ == "__main__":
    boards = cut_boards()
    report_boards(boards)

# Opening in cq-editor
if "show_object" in locals():
    boards = cut_boards()
    show_object(boards[0], boards[1])
    report_boards(boards)


