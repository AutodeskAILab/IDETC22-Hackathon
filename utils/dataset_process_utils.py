import os
from pathlib import Path
from tqdm import tqdm
import json
from collections import Counter
import pandas as pd
import csv


def get_all_files(directory, pattern):
    return [f for f in Path(directory).glob(pattern)]


def save_json(assembly_file, assembly_data, output_dir):
    output = Path(output_dir) / assembly_file.parts[-2] / 'assembly.json'
    os.makedirs(output.parent, exist_ok=True)
    with open(output, "w", encoding="utf8") as f:
        json.dump(assembly_data, f, indent=4)


def read_material_library(data_type):
    with open("materialData.json", "r", encoding="utf-8") as f:
        material_data = json.load(f)

    library_materials = {}
    for library in material_data:
        for material in library["materials"]:
            library_materials[material[data_type]] = material['properties'][11]['value']
    return library_materials


def read_appearance_library():
    return dict(pd.read_csv("appearanceData.csv").values)


def create_csvs():
    with open("stats/labels_default.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["assembly_id", "body_id", "", "material_id",
                         "material_name", "material_appearance_id", "appearance_id",
                         "", "material_label", "material_category", "choice"])

    with open("stats/labels_nonDefault.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["assembly_id", "body_id", "", "material_id",
                         "material_name", "material_appearance_id", "appearance_id",
                         "", "material_label", "material_category", "choice"])

    with open("stats/tier_to_category_mapping.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["tier_1", "tier_2", "tier_3", "count",
                         "", "simplified_category"])

    ################################################################################################

    with open("stats/timeline_default.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["original_id", "appearance_id", "appearance_id_firstSection",
                         "material_appearance_id", "material_app_id_firstSec",
                         "UNKNOWN", "[Label]", "[Category]"])

    with open("stats/timeline_nonDefault.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["original_id", "material_id",
                         "material_name", "material_appearance_id", "material_app_id_firstSec",
                         "appearance_id", "appearance_id_firstSection",
                         "UNKNOWN", "[Label]", "[Category]"])

    ################################################################################################

    with open("stats/tierToSimplifiedCategory_mapping.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(
            ["material_id", "material_name", "material_label", "tier_1", "tier_2", "tier_3", "simplified_category"])


def create_timeline_dicts(appearance_id, material_id, material_name, material_appearance_id):
    dictionary = {"material_id": material_id,
                  "material_name": material_name, "material_appearance_id": material_appearance_id,
                  "material_app_id_firstSec": material_appearance_id.split("_")[0],
                  "appearance_id": appearance_id, "appearance_id_firstSection": appearance_id.split("_")[0],
                  "UNKNOWN": "UNKNOWN"}

    return dictionary


def write_labels_csv(default, input_json, body, material_id, material_name,
                     material_appearance_id, appearance_id, material_label, material_category, choice):
    if default:
        with open("stats/labels_default.csv", 'a', newline='', encoding='utf-8') as f:
            row = [str(input_json).split('\\')[-2],
                   body,
                   "",
                   material_id,
                   material_name,
                   material_appearance_id,
                   appearance_id,
                   "",
                   material_label,
                   material_category,
                   choice]

            writer = csv.writer(f)
            writer.writerow(row)
    else:
        with open("stats/labels_nonDefault.csv", 'a', newline='', encoding='utf-8') as f:

            row = [str(input_json).split('\\')[-2],
                   body,
                   "",
                   material_id,
                   material_name,
                   material_appearance_id,
                   appearance_id,
                   "",
                   material_label,
                   material_category,
                   choice]

            writer = csv.writer(f)
            writer.writerow(row)


def write_timeline_csv(default, material_id, timeline_dict, final_label, final_category):
    if default:
        with open("stats/timeline_default.csv", 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([material_id,
                             timeline_dict["appearance_id"], timeline_dict["appearance_id_firstSection"],
                             timeline_dict["material_appearance_id"], timeline_dict["material_app_id_firstSec"],
                             timeline_dict["UNKNOWN"], final_label, final_category])
    else:
        with open("stats/timeline_nonDefault.csv", 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([material_id, timeline_dict["material_id"], timeline_dict["material_name"],
                             timeline_dict["material_appearance_id"], timeline_dict["material_app_id_firstSec"],
                             timeline_dict["appearance_id"], timeline_dict["appearance_id_firstSection"],
                             timeline_dict["UNKNOWN"], final_label, final_category])


def write_category_mapping_csv(material_id, material_name, material_label, tier_1, tier_2, tier_3, simplified_category):
    with open("stats/tierToSimplifiedCategory_mapping.csv", 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([material_id, material_name, material_label, tier_1, tier_2, tier_3, simplified_category])


def read_autodesk_library():
    # materials_library: <key, val> = <material id, Autodesk material category>
    materials_library = read_material_library("id")

    # materials_library: <key, val> = <material name, Autodesk material category>
    material_name_library = read_material_library("name")

    # appearance_library: <key, val> = <material id, material category>
    appearance_library = read_appearance_library()

    library = {}
    na_num = 0
    for lib in [materials_library, material_name_library, appearance_library]:
        for k, v in list(lib.items()):

            """Deal with special cases - where there is no corresponding Autodesk material category"""
            if k == "4FB9B57A-F157-448C-A618-8861594CD0A6" or k == "F5CEA218-3A0A-4C3D-83AC-171D5B52DA86" or \
                    k == "7972C86C-E1FD-4330-B713-65CA8884391B" or k == "Aluminum - High-Strength Alloy" or \
                    k == "Aluminum - Moderate-Strength Alloy" or k == "Aluminum - Pure (Low-Strength)" or \
                    k == "C5F2133D-0660-40A6-8BA2-BD45E31374EA":
                v = "Autodesk.Material Classifications.Metal.Non Ferrous.Aluminum Alloy"

            if k == "Copper - High-Strength Alloy" or k == "Copper - Pure (Low-Strength)" or \
                    k == "6BEDC50A-1C9B-4400-B9C7-FDAC71BE134B":
                v = "Autodesk.Material Classifications.Metal.Non Ferrous.Copper Alloy"

            if k == "Titanium - High-Strength Alloy" or k == "Titanium - Pure (Low-Strength)" or \
                    k == "4FA3A35A-520F-42E5-988C-62F62BF9AFAE" or k == "ABE903DF-5D7A-4191-9A1F-18B5863BDCDC":
                v = "Autodesk.Material Classifications.Metal.Non Ferrous"

            if k == "Steel - Carbon Steel for Pressure Vessels" or k == "F628A5C3-CA0F-4528-91C7-DABB7B6C5699":
                v = "Autodesk.Material Classifications.Metal.Ferrous.Carbon Steel"

            if k == "Steel - Stainless" or k == "573E7C78-8CC0-40D3-A15F-9F8C107183FA":
                v = "Autodesk.Material Classifications.Metal.Ferrous.Stainless Steel"

            if k == "Steel - High-Strength, Low-Alloy":
                v = "Autodesk.Material Classifications.Metal.Ferrous.Alloy Steel"

            if k == "Plastic" or k == "PrismMaterial-012":
                v = "Autodesk.Material Classifications.Plastic.Thermoplastics"

            if k == "5F9947C7-0FFF-4D9E-80FE-E9A706DE3BB5" or k == "Steel - High-Strength Structural" or \
                    k == "Steel - Standard Structural" or k == "5255369B-8975-49AF-B4E4-D98CE8D2C9CC" or \
                    k == "9F975E36-76A9-4839-8C25-B20D471C7E11":
                v = "Autodesk.Material Classifications.Metal.Ferrous.Carbon Steel"

            v = v.replace("/", ".").replace("Autodesk.Material Classifications.", "").replace(" ", "_")
            library[k] = v

            if not v:
                # print(k)
                na_num += 1

    print(f"[WARNING]: Number of material IDs without valid Autodesk material category label = {na_num}")
    return library
