import pandas as pd
import yaml

paintings = pd.read_csv("paintings.csv").fillna("").to_dict('records')
config = yaml.safe_load(open("config.yml", "r").read())
map_str = ""
scaling_factor = config["scaled_picture_x"] / config["original_picture_x"]

column_offset = {}
column_offset_counter = 0
for column in sorted(config["horizontal_columns"] + config["vertical_columns"]):
    column_offset[column] = column_offset_counter
    if column in config["horizontal_columns"]:
        column_offset_counter += config["horizontal_units_x"]
    else:
        column_offset_counter += config["vertical_units_x"]

for painting in paintings:
    min_x = int((config["total_pixel_offset_x"] + config["pixels_per_unit"] * column_offset[painting["column"]]) * scaling_factor)
    if painting["column"] in config["horizontal_columns"]:
        max_x = int((config["total_pixel_offset_x"] + config["pixels_per_unit"] * (column_offset[painting["column"]] + config["horizontal_units_x"])) * scaling_factor)
        min_y = int((config["total_pixel_offset_y"] + config["pixels_per_unit"] * painting["row"] * config["horizontal_units_y"]) * scaling_factor)
        max_y = int((config["total_pixel_offset_y"] + config["pixels_per_unit"] * (painting["row"]+1) * config["horizontal_units_y"]) * scaling_factor)
    else:
        max_x = int((config["total_pixel_offset_x"] + config["pixels_per_unit"] * (column_offset[painting["column"]] + config["vertical_units_x"])) * scaling_factor)
        min_y = int((config["total_pixel_offset_y"] + config["pixels_per_unit"] * (painting["row"] * config["vertical_units_y"] + config["vertical_column_offset"])) * scaling_factor)
        max_y = int((config["total_pixel_offset_y"] + config["pixels_per_unit"] * ((painting["row"]+1) * config["vertical_units_y"] + config["vertical_column_offset"])) * scaling_factor)

    onclick = f"Popup('{painting['title']}', '{painting['author']}', '{painting['file']}', '{painting['description']}')"
    total = f'    <area shape="rect" coords="{min_x},{min_y},{max_x},{max_y}" onclick="{onclick}" data-toggle="modal" data-target="#infoModal">\n'
    map_str += total

with open("index.html", "w") as f:
    f.write(open("html_pre.txt", "r").read())
    f.write(map_str)
    f.write(open("html_post.txt", "r").read())