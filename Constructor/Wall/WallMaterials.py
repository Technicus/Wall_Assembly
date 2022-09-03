#!/usr/bin/env python3
# version beta

# Material data

import csv
from cadquery import Sketch, Workplane


class Board:
    def __init__(self, name, profile, length):
        self.name = name
        self.profile = profile
        self.length = length
        self.sketch = Sketch()
        self.workplane = Workplane()


    def profile_set(self):
        if self.profile == None:
            return None
        with open('./Profiles/lumbar.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            for row in csv_reader:
                if row:
                    if row[0] == self.profile:
                        return (row[0], float(row[1]), float(row[2]), float(row[3]), row[4])


    # Create board sketch profiles.
    def build_sketch(self):
        self.sketch().rect(self.profile_set(self)[1], self.profile_set(self)[2]).vertices().fillet(self.profile_set(self)[3])
        self.workplane().placeSketch(self.sketch).extrude(self.length)


    def show_board(self):
        show_object(self, "board_stud")





print(f"\nBoard:")

board = Board('stud', '2x4', (114.5, 'in'))
board.show_board()
#show_object(board, "board_stud")


print(f"\n\tname:\t(\'{board.name}\')")
print(f"\tprofile:{board.profile_set()}")
print(f"\tlength:\t{board.length}")
print(f"")



#print(f"\n\t{board.dict}")
#print(f"type:\n\t{type(board)}")
#print(f"dir:\n\t{dir(board)}")
#print(f"__dir__:\n\t{board.__dir__}")
#print(f"__format__:\n\t{board.__format__}")
#print(f"__dict__:\n\t{board.__dict__}")
#print(f"profile:\t{board.profile}")
#print(f"_fieldnames:\n\t{board._fieldnames}")
#print(f"dialect:\n\t{board.dialect}")
#print(f"fieldnames:\n\t{board.fieldnames}")
#print(f"line_num:\n\t{board.line_num}")
#print(f"reader:\n\t{board.reader}")
#print(f"dir(board.reader):\n\t{dir(board.reader)}")
#print(f"restkey:\n\t{board.restkey}")
#print(f"restval:\n\t{board.restval}")


#lumbar_profile = lumbar_profile_set('print')
#lumbar_profile = lumbar_profile_set('4x4')
#print(f"\n\t{lumbar_profile}")




#def board_profile(board_dimensions = None):
    #if board_dimensions  == '2x4':
        ## Set board dimentions for dimentional lumbar in metric
        #profile = {
            #"width": 38,
            #"depth": 89,
            #"radius": 3.2
        #}
        #return profile
    #if board_dimensions  == '2x6':
        #profile = {
            #"width": 38,
            #"depth": 140,
            #"radius": 3.2
        #}
        #return profile


        ## This portion of function is for development purposes and should eventually be removed
        #if self.profile == 'print':
            #with open('./Profiles/lumbar.csv') as csv_file:
                #csv_reader = csv.reader(csv_file, delimiter=';')
                #line_count = 0
                #for row in csv_reader:
                    #if row:
                        #if line_count == 0:
                            ##print(f"\n\t{' '.join(row)}\n")
                            #print(f'\n\t{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\n')
                            #line_count += 1
                        #else:
                            #print(f'\t{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}')
                            #line_count += 1
                #print(f'\n\tProcessed {line_count} lines.')
                #return None
                    #if row[0] == 'PROFILE':
                        #print(f'\n\t{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}')
                        #print(f'\t{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}')


 #.extrude(2984.7)
        #board_stud_profile = (
            #Sketch()
            #.rect(board_profile(wall_parameters.stud_profile)["width"], board_profile(wall_parameters.stud_profile)["depth"])
            #.vertices()
            #.fillet(board_profile(wall_parameters.stud_profile)["radius"])
        #)

    ## Create the boards and match them to length for wall.
    #board_wall_stud = (
        #Workplane()
        #.placeSketch(board_stud_profile)
        ##.extrude(2984.7)
        #.extrude(wall_parameters.board_length["studs"])
        ##.extrude(board_profile(wall_parameters.height - board_profile(wall_parameters.top_plate_profile)["width"] - board_profile(wall_parameters.bottom_plate_profile)["width"]))
    #)
