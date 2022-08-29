#!/usr/bin/env python3
from cadquery import exporters, Sketch, Workplane, Assembly, Color

#s = Workplane("XY")
#sPnts = [
    #(2.75, 1.5),
    #(2.5, 1.75),
    #(2.0, 1.5),
    #(1.5, 1.0),
    #(1.0, 1.25),
    #(0.5, 1.0),
    #(0, 1.0)
#]
#r = s.lineTo(3.0, 0).lineTo(3.0, 1.0).spline(sPnts, includeCurrent=True).close()
#result = r.extrude(0.5)

result = (Workplane("front").box(3.0, 4.0, 0.25).pushPoints([(0, 0.75), (0, -0.75)])
    .polygon(6, 1.0).cutThruAll())


#scene = Assembly(None, name="svg_scene")
#scene.add(result, name="result")

exporters.export(
    #scene.toCompound(),
    result,
    "../Exports/Info/combination/result_03.svg",
    opt={
        "width": 1200,
        "height": 768,
        "marginLeft": 10,
        "marginTop": 10,
        #"showAxes": True,
        "projectionDir": (5, -5, 1),
        "strokeWidth": 0.5,
        "strokeColor": (0, 0, 0),
        "hiddenColor": (0, 0, 0),
        "showHidden": True,
    },
    #exporters.ExportTypes.SVG,
)
