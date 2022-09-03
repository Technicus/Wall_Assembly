#!/usr/bin/env python3
# version beta

# Export configs

def dimension_wall(wall = None):
    # Create drawing instance with appropriate settings
    #metric_drawing = Draft(decimal_precision=1)

    ## Create an extension line from corners of the part
    #length_dimension_line = metric_drawing.extension_line(
        #object_edge=wall.faces("<Z").vertices("<Y").vals(),
        #offset=10.0,
        #tolerance=(+0.2, -0.1),
    #)

    #if "show_object" in locals():
        #show_object(mystery_object, name="mystery_object")
        #show_object(length_dimension_line, name="length_dimension_line")  .
    #front_dimensions = Draft(font_size=10, decimal_precision=0, label_normal=(0, -1, 0))
    ##width_dl = front_dimensions.extension_line(object_edge=width_vertices, offset=10.0)

    #height_dl = front_dimensions.extension_line(
        #object_edge = wall.cq_object.objects["right_stile"]
        #.obj.edges(">X and <Y")
        #.val(),
        #offset=-10.0,
    #)

    #dimension_lines = cq.Assembly(None, name="dimension_lines")
    #dimension_lines.add(width_dl, name="width")
    #dimension_lines.add(height_dl, name="height")

    return wall_dimension
