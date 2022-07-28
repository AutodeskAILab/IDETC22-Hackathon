"""
Filter out ONLY the PNG and JSON files from the original assembly dataset
"""
import os
import shutil
import glob
from tqdm import tqdm
import json
from PIL import Image, ImageDraw, ImageFont


def transfer_png_json(original_dataset_path, current_dataset_path):
    """
    Transfer PNG files AND json files for each body of each assembly
    """

    if os.path.exists(current_dataset_path):
        shutil.rmtree(current_dataset_path)
    os.mkdir(current_dataset_path)

    current_assemblies = os.listdir(original_dataset_path)
    original_assemblies = os.listdir(original_dataset_path)

    counter = 0

    for current_assembly in tqdm(current_assemblies, desc="Transferring the PNG and JSON files..."):
        for original_assembly in original_assemblies:
            if original_assembly == current_assembly:

                os.mkdir(current_dataset_path + '\\' + current_assembly)

                for pngfile in glob.iglob(os.path.join(original_dataset_path + '\\' + original_assembly, "*.png")):
                    shutil.copy(pngfile, current_dataset_path + '\\' + current_assembly)

                for jsonfile in glob.iglob(os.path.join(original_dataset_path + '\\' + original_assembly, "*.json")):
                    shutil.copy(jsonfile, current_dataset_path + '\\' + current_assembly)
        counter += 1

    print("Finished transferring the PNG and JSON files for:", counter, "assemblies")


def rename_assembly_png(current_dataset_path):
    """
    Rename the assembly PNG files, add additional info (e.g, assembly name and total number of bodies from JSON)
    """

    current_assemblies = os.listdir(current_dataset_path)

    counter = 0

    for current_assembly in tqdm(current_assemblies, desc="Renaming the assembly.png to corresponding ID..."):

        for json_file in glob.iglob(os.path.join(current_dataset_path + '\\' + current_assembly, "assembly.json")):
            with open(json_file, "r", encoding="utf-8") as f:
                assembly_data = json.load(f)

                # Number of bodies
                body_num = len(assembly_data["bodies"])

        current_assembly_path = current_dataset_path + '\\' + current_assembly + '\\' + "assembly.png"

        # Add body num info
        font_title = ImageFont.truetype("C:\Windows\Fonts\Calibri.ttf", 40)
        assembly_png = Image.open(current_assembly_path)
        draw = ImageDraw.Draw(assembly_png)
        text = "[Total number of bodies]: " + str(body_num)
        draw.text((60, 40), text, (255, 0, 0), font=font_title)
        save_path = current_dataset_path + '\\' + current_assembly + '\\' + "assembly.png"
        assembly_png.save(save_path)

        for pngfile in glob.iglob(os.path.join(current_dataset_path + '\\' + current_assembly, "assembly.png")):
            os.rename(pngfile, "Generated_assembly_filtering" + '\\' + current_assembly + ".png")
            counter += 1

    print("Number of PNG files renamed: ", counter)


if __name__ == "__main__":

    # TODO: specify the directory to the assembly dataset down belo
    from_path = "C:\\Users\\bians\\OneDrive - Autodesk\\Desktop\\dataset\\assembly"
    to_path = "filtered_dataset"

    transfer_png_json(from_path, to_path)
