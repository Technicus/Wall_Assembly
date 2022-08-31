# Wall_Assembly
This is a utility to generate architectural drawings and 3d models for wall assemblies.

# examples:
- clear; ./WallConstructor.py --length 8ft --height 120.5in --stud_spacing 16in --stud_profile 2x4 --bottom_plate_profile 2x6 --top_plate_profile 2x4
- clear; ./WallConstructor.py --length 10ft --height 90.5in --stud_spacing 24in --stud_profile 2x4 --bottom_plate_profile 2x6 --top_plate_profile 2x4

# currently works
- accepting parameters
- generating boards from dimensional lumbar profiles
- unit conversion
- assembling wall frame
- exporting to stl
- exporting to step

# current development
- trying to understand svg export viewing angles
- trying to add dimensions

# todo:
- need to integrate accountability for number stud center offset, stud spacing start (before first stud, first stud, after first stud), and stud count past length of wall
- add name to accepted parameters
- add export file type to parameters
- add web interface to accept parameters
- embed 3d view in web interface
- add more input validateion
- define more lumbar profiles
- create mechanism and parameters for defining and crafting openings
- create a cut list export
- create dxf and pdf export for 2d view of a render with dimensions to generate architectural drawings
- do more construction testing with various parameter options
- refine constraints
- add additional elements like sheeting, external layers, insulation, and internal layers

