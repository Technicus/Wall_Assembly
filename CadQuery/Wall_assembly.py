#!/usr/bin/env python3


import cadquery as cq

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
    "stud_distribution": 406.4, # 16"
    "stud_count": 6 # bottom_plate_length / stud_distribution round up
}

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

# Tag mating edges
board_wall_stud.faces("<Z").tag("stud_bottom")
board_bottom_plate.faces(">X").tag("bottom_plate_top")

# Create the wall assembly.
wall = (
    cq.Assembly()
)

#wall.add(
    #board_bottom_plate,
    #loc = cq.Location(cq.Vector(0, 0, 0), cq.Vector(1, 0, 0), 90),
    #name = "bottom_plate",
    #color= cq.Color("green")
    #)

#wall.add(
    #board_wall_stud,
    ##loc = cq.Location(cq.Vector(0, 0, 0), cq.Vector(1, 0, 0), 180),
    #name = "stud",
    #color=cq.Color("brown")
    #)

board_bottom_plate = board_bottom_plate.rotate((0,0,0), (0,1,0), 90)

wall = (
        cq.Assembly()
        .add(board_bottom_plate, name="board_bottom_plate", color=cq.Color("green"))
        .add(board_wall_stud, name="stud0", color=cq.Color("brown"))
        .add(board_wall_stud, name="stud1", color=cq.Color("brown"))
        .constrain("board_bottom_plate", "Fixed")
        .constrain("stud0", "FixedRotation", (0,0,0))
        .constrain("stud1", "FixedRotation", (0,0,0))

        .constrain("stud0?stud_bottom", "board_bottom_plate@faces@>Z", "PointInPlane")
        .constrain("stud1?stud_bottom", "board_bottom_plate@faces@>Z", "PointInPlane")

        .constrain("board_bottom_plate@faces@<X", "stud0@faces@<X", "PointInPlane", 0)
        .constrain("board_bottom_plate@faces@<X", "stud1@faces@<X", "PointInPlane", 380)

        .constrain("board_bottom_plate@faces@>Y", "stud0@faces@>Y", "PointInPlane", 0)
        .constrain("board_bottom_plate@faces@>Y", "stud1@faces@>Y", "PointInPlane", 0)
)

wall.solve()

show_object(wall)
