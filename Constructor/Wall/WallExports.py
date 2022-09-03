#!/usr/bin/env python3
# version beta

# Export configs
from cadquery import exporters, Sketch, Workplane, Assembly, Color


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


def file_count(dir_path = None):
    count = 0
    #dir_path = r'../../'
    for path in scandir(dir_path):
        if path.is_file():
            count += 1
    #print('file count:', count)
    #count = f'{count:02d}'
    return f'{count:02d}'

#def file_check(file_exam = None):
    #file_to_check = Path(file_exam)

    #if file_to_check.is_file():
        #print(f'The file {file_exam} exists')
        #return file_exam +
    #else:
        #print(f'The file {file_exam} does not exist')
        #return file_exam


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
