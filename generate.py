import pandas as pd
import yaml
from collections import defaultdict

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

artist_count = defaultdict(int)
for painting in paintings:
    min_x = int((config["total_pixel_offset_x"] + config["pixels_per_unit"] * column_offset[painting["column"]]) * scaling_factor)
    if painting["column"] in config["horizontal_columns"]:
        max_x = int((config["total_pixel_offset_x"] + config["pixels_per_unit"] * (column_offset[painting["column"]] + config["horizontal_units_x"])) * scaling_factor)
        min_y = int((config["total_pixel_offset_y"] + config["pixels_per_unit"] * painting["row"] * config["horizontal_units_y"]) * scaling_factor)
        max_y = int((config["total_pixel_offset_y"] + config["pixels_per_unit"] * (painting["row"]+1) * config["horizontal_units_y"]) * scaling_factor)
        dir = "H"
    else:
        max_x = int((config["total_pixel_offset_x"] + config["pixels_per_unit"] * (column_offset[painting["column"]] + config["vertical_units_x"])) * scaling_factor)
        min_y = int((config["total_pixel_offset_y"] + config["pixels_per_unit"] * (painting["row"] * config["vertical_units_y"] + config["vertical_column_offset"])) * scaling_factor)
        max_y = int((config["total_pixel_offset_y"] + config["pixels_per_unit"] * ((painting["row"]+1) * config["vertical_units_y"] + config["vertical_column_offset"])) * scaling_factor)
        dir = "V"

    safe_description = painting["description"].replace("'", "\\\'")
    onclick = f"Popup('{painting['title']}', '{painting['author']}', '{painting['file']}', '{safe_description}', '{dir}')"
    total = f'      <area shape="rect" coords="{min_x},{min_y},{max_x},{max_y}" onclick="{onclick}">\n'
    map_str += total

    artist_count[painting["author"]] += 1

artist_str = ""
for artist in sorted(artist_count.keys(), key=lambda x: artist_count[x], reverse=True):
    artist_str += f"            <p><b>{artist}</b>: {artist_count[artist]}</p>"

with open("index.html", "w") as f:
    html = open("html_template.txt", "r").read()
    html = html.replace("IMAGEMAPINSERT", map_str)
    html = html.replace("ARTISTMODALINSERT", artist_str)
    f.write(html)
