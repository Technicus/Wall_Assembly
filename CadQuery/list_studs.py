#!/usr/bin/env python3

import math

length_baseplate = 100
distance_between_studs = 9
number_studs = (length_baseplate / distance_between_studs)
number_studs_round_up = math.ceil(number_studs)
number_studs_round_down = math.floor(number_studs)
print(number_studs)
print(int(number_studs))
print(number_studs_round_up)
print(number_studs_round_down)
studs = []
for x in range(int(number_studs)):
    studs.append("stud_"+str(x))
print(studs)
