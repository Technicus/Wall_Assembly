#! /bin/bash

# for i in '../Exports/Drawings/evaluate/png/*.png'; do
# #     time = $(echo $i | cut -d . -f 1)
# #     echo $i
#     ffmpeg -i $i -vf "drawtext=text=$i" mod-$i.png
# done

subprocess.call("ffmpeg -framerate 60 -pattern_type glob -i '../Exports/Drawings/evaluate/png/*.png' -c:v libx264 -pix_fmt yuv420p out.mp4")

"ffmpeg -framerate 30 -pattern_type glob -i '../Exports/Drawings/evaluate/png/*.png' -c:v libx264 -pix_fmt yuv420p out.mp4"

"ffmpeg -framerate 60 -pattern_type glob -i '../Exports/Drawings/evaluate/png/*.png' -c:v libx264 -pix_fmt yuv420p out.mp4"

# ffmpeg \
#     -f image2 \
#     -pattern_type glob \
#     -export_path_metadata 1 \
#     -i '../Exports/Drawings/evaluate/png/*.png' \
#     -vf "drawtext=text='%{metadata\:lavf.image2dec.source_basename\:NA}'" \
#     -y '../Exports/Drawings/evaluate/png/output.mkv'
