#!/usr/bin/env python3

import math

wall_parameters = {
    "stud_length": 2908.3, # 114.5"
    "bottom_plate_length": 2438, # 8'
    "top_plate_length": 2438, # 8'
    "stud_distribution": 406.4, # 16"
    "stud_count": 0,
    "studs": []
}

wall_parameters["stud_count"] = math.floor(wall_parameters["bottom_plate_length"] / wall_parameters["stud_distribution"]) + 2
studs = []
for x in range(int(wall_parameters["stud_count"])):
    wall_parameters["studs"].append("stud_"+str(x))

print(int(wall_parameters["stud_count"]))
print(wall_parameters["studs"])
print(wall_parameters["studs"][1:-1])

for stud in range(len(wall_parameters["studs"][1:-1])):
    print(wall_parameters["studs"][stud + 1])
