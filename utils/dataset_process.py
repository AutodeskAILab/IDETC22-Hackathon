"""
Process the JSON files in the assembly dataset in the following ways:
    - image_size_reduction: reduce the size of the PNG files, and change to JPG format
    -
"""
import os
import shutil
import glob
from tqdm import tqdm
import json
import cv2
from PIL import Image, ImageDraw, ImageFont
from utils.dataset_process_utils import *

MAPPINGS = []


def image_size_reduction(path):
    assemblies = os.listdir(path)

    for assembly in tqdm(assemblies, desc="Reducing the size of image files"):
        for pngfile in glob.iglob(os.path.join(path + '\\' + assembly, "*.png")):
            # 1024 x 1024 -> 512 x 512
            img = Image.open(pngfile)
            img = img.resize((512, 512), Image.ANTIALIAS)

            img = img.convert("RGB")
            img.save(pngfile.split('.')[0] + '.jpg', optimize=True, quality=85)
            img.close()

            # .png -> .jpg
            os.remove(pngfile)


def map_bodies(jsons, library, output_dir):
    counter_material = []
    counter_material_label = []
    counter_simple_cat = []
    counter_all_default_materials = 0

    if os.path.exists("stats"):
        shutil.rmtree("stats")
    os.makedirs("stats", exist_ok=True)

    create_csvs()

    for input_json in tqdm(jsons, desc='Mapping bodies and saving output'):

        with open(input_json, "r", encoding="utf-8") as f:
            assembly_data = json.load(f)
        bodies = assembly_data['bodies'].keys()
        default_material_count = 0

        for body in bodies:
            appearance_id = assembly_data['bodies'][body]["appearance"]["id"]
            material_id = assembly_data['bodies'][body]["material"]["id"]
            material_name = assembly_data['bodies'][body]["material"]["name"]
            material_appearance_id = assembly_data['bodies'][body]["material"]["appearance"]["id"]

            timeline_dict = create_timeline_dicts(appearance_id, material_id, material_name, material_appearance_id)

            if material_id != "PrismMaterial-018":
                default = False
                # The body material id is not default, we prioritize true material over appearance
                # material id -> first part of material id -> material name ->
                # material_appearance_id -> first part of material_appearance_id ->
                # appearance id -> first part of appearance id -> UNKNOWN
                try:
                    material_category = library[material_id]
                    material_label = material_id
                    choice = "material_id"
                    timeline_dict["material_id"] = f"[{material_id}]"
                except KeyError:
                    # try:
                    #     material_category = library[material_id.split("_")[0]]
                    #     material_label = material_id.split("_")[0]
                    #     choice = "material_id_firstSec"
                    # except KeyError:
                    try:
                        material_category = library[material_name]
                        material_label = material_id
                        choice = "material_id"
                        timeline_dict["material_name"] = f"[{material_name}]"
                    except KeyError:
                        try:
                            material_category = library[material_appearance_id]
                            material_label = material_appearance_id
                            choice = "material_app_id"
                            timeline_dict["material_appearance_id"] = f"[{material_appearance_id}]"
                        except KeyError:
                            try:
                                material_category = library[material_appearance_id.split("_")[0]]
                                material_app_id_firstSec = material_appearance_id.split("_")[0]
                                material_label = material_app_id_firstSec
                                choice = "material_app_id_firstSec"
                                timeline_dict["material_app_id_firstSec"] = f"[{material_app_id_firstSec}]"
                            except KeyError:
                                try:
                                    material_category = library[appearance_id]
                                    material_label = appearance_id
                                    choice = "app_id"
                                    timeline_dict["appearance_id"] = f"[{appearance_id}]"
                                except KeyError:
                                    try:
                                        material_category = library[appearance_id.split("_")[0]]
                                        app_id_firstSec = appearance_id.split("_")[0]
                                        material_label = app_id_firstSec
                                        choice = "app_id_firstSec"
                                        timeline_dict["appearance_id_firstSection"] = f"[{app_id_firstSec}]"
                                    except KeyError:
                                        material_category = 'Unknown'
                                        material_label = material_id
                                        choice = "material_id_UNKNOWN"
                                        timeline_dict["UNKNOWN"] = f"[UNKNOWN]"
            else:
                default = True
                # The body material ID is default, so we prioritize appearance over true material
                # appearance id -> first part of appearance id ->
                # material appearance id -> first part of material appearance id ->
                # material id -> first part of material id -> material name -> UNKNOWN
                try:
                    # examine the appearance id
                    material_category = library[appearance_id]
                    material_label = appearance_id
                    choice = "app_id"
                    timeline_dict["appearance_id"] = f"[{appearance_id}]"
                except KeyError:
                    try:
                        # examine the first part of the appearance id
                        material_category = library[appearance_id.split("_")[0]]
                        app_id_firstSec = appearance_id.split("_")[0]
                        material_label = app_id_firstSec
                        choice = "app_id_firstSec"
                        timeline_dict["appearance_id_firstSection"] = f"[{app_id_firstSec}]"
                    except KeyError:
                        try:
                            # examine the material appearance id
                            material_category = library[material_appearance_id]
                            material_label = material_appearance_id
                            choice = "material_app_id"
                            timeline_dict["material_appearance_id"] = f"[{material_appearance_id}]"
                        except KeyError:
                            try:
                                # examine the first part of the material appearance id
                                # TODO: all material_appearance_id == PrismMaterial-018_physmat_aspects:Prism-25
                                material_category = library[material_appearance_id.split("_")[0]]
                                material_app_id_firstSec = material_appearance_id.split("_")[0]
                                material_label = material_app_id_firstSec
                                choice = "material_app_id_firstSec"
                                timeline_dict["material_app_id_firstSec"] = f"[{material_app_id_firstSec}]"
                            except KeyError:
                                try:
                                    # material_app_id = 74F0DAFA-4EB4-40EE-8CF6-36F014197DC9
                                    # TODO: not executing here and below at all?
                                    material_category = library[material_id]
                                    material_label = material_id
                                    choice = "material_id"
                                    timeline_dict["material_id"] = f"[{material_id}]"
                                except KeyError:
                                    # try:
                                    #     material_category = library[material_id.split("_")[0]]
                                    #     material_label = material_id.split("_")[0]
                                    #     choice = "material_id_firstSec"
                                    # except KeyError:
                                    try:
                                        material_category = library[material_name]
                                        material_label = material_id
                                        choice = "material_id"
                                        timeline_dict["material_name"] = f"[{material_name}]"
                                    except KeyError:
                                        material_category = 'Unknown'
                                        material_label = material_id
                                        choice = "material_id_UNKNOWN"
                                        timeline_dict["UNKNOWN"] = f"[UNKNOWN]"

            if material_label == 'PrismMaterial-018' or material_label == "PrismMaterial-018_physmat_aspects:Prism-256":
                default_material_count += 1

            if material_category == "":
                # in this case, all tiers will be "Unknown"
                material_category = 'Unknown'

            tier1 = material_category.split(".")[0]
            try:
                tier2 = material_category.split(".")[1]
            except IndexError:
                tier2 = 'Unknown'
            try:
                tier3 = material_category.split(".")[2]
            except IndexError:
                tier3 = 'Unknown'

            # save stats to CSV

            write_labels_csv(default, input_json, body, material_id, material_name,
                             material_appearance_id, appearance_id, material_label, material_category, choice)

            write_timeline_csv(default, material_id, timeline_dict, material_label, material_category)

            # save results to JSON and update

            assembly_data['bodies'][body]["material_category"] = {"tier1": tier1, "tier2": tier2, "tier3": tier3}
            counter_material.append(material_category)

        save_json(input_json, assembly_data, output_dir)

    return counter_material, counter_material_label, counter_all_default_materials, counter_simple_cat


def clean_features(jsons, output_dir):
    for input_json in tqdm(jsons, desc='Cleaning JSON features'):
        with open(input_json, "r", encoding="utf-8") as f:
            assembly_data = json.load(f)
        bodies = assembly_data['bodies'].keys()

        for body in bodies:
            del assembly_data['bodies'][body]["type"]
            del assembly_data['bodies'][body]["smt"]
            del assembly_data['bodies'][body]["step"]
            del assembly_data['bodies'][body]["obj"]
            del assembly_data['bodies'][body]["appearance"]
            del assembly_data['bodies'][body]["material"]

            png = assembly_data['bodies'][body]["png"]
            del assembly_data['bodies'][body]["png"]
            assembly_data['bodies'][body]["jpg"] = png.split(".")[0] + ".jpg"

        save_json(input_json, assembly_data, output_dir)


if __name__ == "__main__":
    """ Process Step 1: Reducing image size"""
    # image_size_reduction("filtered_dataset")

    """ Process Step 2: Generating hierarchical material_category for JSONs"""
    # input_dir = "../IDETC22-Hackathon-Dataset"
    # output_dir = "processed_result"
    #
    # library_material = read_autodesk_library()
    # input_jsons = get_all_files(input_dir, "*/assembly.json")
    #
    # map_bodies(input_jsons, library_material, output_dir)

    """ Process Step 3: Cleaning up the features in the JSONs"""
    input_dir = "../IDETC22-Hackathon-Dataset"
    output_dir = "processed_result"
    input_jsons = get_all_files(input_dir, "*/assembly.json")

    clean_features(input_jsons, output_dir)
