#!/usr/bin/env python3


import cadquery as cq

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

wall_dimensions = {
    "stud": 2908.3,
    "bottom_plate": 2438
}

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

board_wall_stud = (
    cq.Workplane()
    .placeSketch(board_profile_2x4)
    .extrude(wall_dimensions["stud"])
)

# tag mating edges
board_wall_stud.faces("<Z").tag("stud_bottom")

board_bottom_plate = (
    cq.Workplane()
    .placeSketch(board_profile_2x6)
    .extrude(wall_dimensions["bottom_plate"])
)

# tag mating edges
board_bottom_plate.faces(">X").tag("bottom_plate_top")


wall = (
        cq.Assembly()
)



show_object(board_wall_stud, options = dict(alpha = 0.0, color = ("brown")))
show_object(board_bottom_plate, options = dict(alpha = 0.0, color = ("green")))
