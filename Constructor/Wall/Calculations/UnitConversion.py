#!/usr/bin/env python3
# version beta

"""
Unit Conversion Calculator

name: UnitConversion.py
by:   Technicus
date: September 3st 2022

desc: This python/cadquery code is a component of the larger architectural development concept, "ProjectDesignBuilder".

license:
    Copyright 2022 Technicus

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""


#from re import findall, split, finditer

# A unit conversion function that accepts an input value, units for that value and the desired conversion unit.
# Input validation should be implemented
def unit_conversion(length = float(0), in_units = None, out_units = None):
    if in_units == 'in':
        if out_units == 'in':
            return length, out_units
        if out_units == 'ft':
            return length / 12, out_units
        if out_units == 'yd':
            return length / 36, out_units
        if out_units == 'mm':
            return length * 25.4, out_units
        if out_units == 'cm':
            return length * 2.54, out_units
        if out_units == 'm':
            return length * 0.0254, out_units
        if out_units == 'px':
            return length * 96, out_units
        if out_units == 'py':
            return length * 96, out_units

    if in_units == 'ft':
        if out_units == 'in':
            return length * 12, out_units
        if out_units == 'ft':
            return length, out_units
        if out_units == 'yd':
            return length / 3, out_units
        if out_units == 'mm':
            return length * 304.8, out_units
        if out_units == 'cm':
            return length * 30.48, out_units
        if out_units == 'm':
            return length * 0.3048, out_units
        if out_units == 'px':
            return length * 12 * 96, out_units
        if out_units == 'py':
            return length * 12 * 96, out_units

    if in_units == 'yd':
        if out_units == 'in':
            return length * 36, out_units
        if out_units == 'ft':
            return length * 3, out_units
        if out_units == 'yd':
            return length, out_units
        if out_units == 'mm':
            return length * 9.144, out_units
        if out_units == 'cm':
            return length * 91.44, out_units
        if out_units == 'm':
            return length * 0.9144, out_units
        if out_units == 'px':
            return length * 36 * 96, out_units
        if out_units == 'py':
            return length * 36 * 96, out_units

    if in_units == 'mm':
        if out_units == 'in':
            return length / 25.4, out_units
        if out_units == 'ft':
            return length / 304.8, out_units
        if out_units == 'yd':
            return length /9.144, out_units
        if out_units == 'mm':
            return length, out_units
        if out_units == 'cm':
            return length / 10, out_units
        if out_units == 'm':
            return length / 1000, out_units
        if out_units == 'px':
            return length * 3.7795275591, out_units
        if out_units == 'py':
            return length * 3.7795275591, out_units

    if in_units == 'cm':
        if out_units == 'in':
            return length / 2.54, out_units
        if out_units == 'ft':
            return length / 30.48, out_units
        if out_units == 'yd':
            return length / 91.44, out_units
        if out_units == 'mm':
            return length * 10, out_units
        if out_units == 'cm':
            return length, out_units
        if out_units == 'm':
            return length / 100, out_units
        if out_units == 'px':
            return length * 37.795275591, out_units
        if out_units == 'py':
            return length * 37.795275591, out_units

    if in_units == 'm':
        if out_units == 'in':
            return length / 0.0254, out_units
        if out_units == 'ft':
            return length * 3.280839895, out_units
        if out_units == 'yd':
            return length / 0.9144, out_units
        if out_units == 'mm':
            return length * 1000, out_units
        if out_units == 'cm':
            return length * 100, out_units
        if out_units == 'm':
            return length, out_units
        if out_units == 'px':
            return length * 3779.5275591, out_units
        if out_units == 'py':
            return length * 3779.5275591, out_units

    if in_units == 'px':
        if out_units == 'in':
            return length / 0.0254, out_units
        if out_units == 'ft':
            return length * 3.280839895, out_units
        if out_units == 'yd':
            return length / 0.9144, out_units
        if out_units == 'mm':
            return length * 1000, out_units
        if out_units == 'cm':
            return length * 100, out_units
        if out_units == 'm':
            return length, out_units
        if out_units == 'px':
            return length, out_units
        if out_units == 'py':
            return length, out_units

    if in_units == 'py':
        if out_units == 'in':
            return length / 0.0254, out_units
        if out_units == 'ft':
            return length * 3.280839895, out_units
        if out_units == 'yd':
            return length / 0.9144, out_units
        if out_units == 'mm':
            return length * 1000, out_units
        if out_units == 'cm':
            return length * 100, out_units
        if out_units == 'm':
            return length, out_units
        if out_units == 'px':
            return length, out_units
        if out_units == 'py':
            return length, out_units
