#!/usr/bin/env python3


import cadquery as cq
import math

# Set board dimentions for dimentional lumbar in metric
board_dimensions_2x4 = {
    "width": 38,
    "depth": 89,
    "radius": 3.2
}

board_dimensions_2x6 = {
    "width": 38,
    "depth": 140,
    "radius": 3.2
}

# Set wall dimentions, material lengths, number of studs.
# todo: include parameters for openings, corners and additional features.
wall_parameters = {
    "stud_length": 2908.3, # 114.5"
    "bottom_plate_length": 2438, # 8'
    "top_plate_length": 2438, # 8'
    "stud_spacing": 406.4, # 16"
    "stud_count": 0, # bottom_plate_length / stud_spacing round up
    "studs": []
}

wall_parameters["stud_count"] = math.floor(wall_parameters["bottom_plate_length"] / wall_parameters["stud_spacing"]) + 2
studs = []
for x in range(int(wall_parameters["stud_count"])):
    wall_parameters["studs"].append("stud_"+str(x))

# Create board sketch profiles.
board_profile_2x4 = (
    cq.Sketch()
    .rect(board_dimensions_2x4["width"], board_dimensions_2x4["depth"])
    .vertices()
    .fillet(board_dimensions_2x4["radius"])
)

board_profile_2x6 = (
    cq.Sketch()
    .rect(board_dimensions_2x6["width"], board_dimensions_2x6["depth"])
    .vertices()
    .fillet(board_dimensions_2x6["radius"])
)

# Create the boards and match them to length for wall.
board_wall_stud = (
    cq.Workplane()
    .placeSketch(board_profile_2x4)
    .extrude(wall_parameters["stud_length"])
)

board_bottom_plate = (
    cq.Workplane()
    .placeSketch(board_profile_2x6)
    .extrude(wall_parameters["bottom_plate_length"])
)

board_top_plate = (
    cq.Workplane()
    .placeSketch(board_profile_2x4)
    .extrude(wall_parameters["top_plate_length"])
)

# Create the wall assembly.
wall = (
    cq.Assembly()
)

board_bottom_plate = board_bottom_plate.rotate((0,0,0), (0,1,0), 90)
board_top_plate = board_top_plate.rotate((0,0,0), (0,1,0), 90)

wall = (
    cq.Assembly()
    .add(board_bottom_plate,
    #loc=cq.Location(cq.Vector(0, 0, 0), cq.Vector(0, 1, 0), 90),
    name = "board_bottom_plate",
    color = cq.Color("green"))
)

wall.add(
    board_top_plate,
    name = "board_top_plate",
    color = cq.Color("brown"))

for stud in wall_parameters["studs"]:
    wall.add(
        board_wall_stud,
        name = stud,
        color = cq.Color("brown"))

for stud in wall_parameters["studs"]:
    wall.constrain(stud, "FixedRotation", (0, 0, 0))

for stud in wall_parameters["studs"]:
    wall.constrain(f"{stud}@faces@<Z", "board_bottom_plate@faces@>Z", "PointInPlane")
    wall.constrain("board_bottom_plate@faces@>Y", f"{stud}@faces@>Y", "PointInPlane", 0)

wall.constrain(f"{wall_parameters['studs'][0]}@faces@<X", "board_bottom_plate@faces@<X", "PointInPlane")
wall.constrain(f"{wall_parameters['studs'][-1]}@faces@>X", "board_bottom_plate@faces@>X", "PointInPlane")

for stud in range(len(wall_parameters["studs"][1:])):
    stud_spacing = wall_parameters["stud_spacing"] * stud
    wall.constrain("board_bottom_plate@faces@<X", f"{wall_parameters['studs'][stud]}@faces@<X", "PointInPlane", stud_spacing)

wall.constrain("board_top_plate@faces@<X",f"{wall_parameters['studs'][0]}@faces@<X",  "PointInPlane")
wall.constrain("board_top_plate@faces@>X",f"{wall_parameters['studs'][-1]}@faces@>X",  "PointInPlane")
wall.constrain("board_top_plate@faces@<Z", f"{wall_parameters['studs'][0]}@faces@>Z", "PointInPlane")
wall.constrain("board_top_plate@faces@>Y", f"{wall_parameters['studs'][0]}@faces@>Y", "PointInPlane")
wall.constrain("board_top_plate@faces@<Y", f"{wall_parameters['studs'][0]}@faces@<Y", "PointInPlane")

wall.solve()

show_object(wall)

