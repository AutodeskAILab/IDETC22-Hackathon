import argparse
import sys
import os
import glob
import shutil
from tqdm import tqdm


def extraction(args):
    assemblies = os.listdir(args.input)

    if args.feature == "assembly_json":
        print("Extracting assembly JSON files from assemblies")
        out_dir = "./assembly-jsons"
    elif args.feature == "assembly_thumbnail":
        print("Extracting assembly thumbnail PNG files from assemblies")
        out_dir = "./assembly-thumbnails"
    else:
        print("Extracting body thumbnail PNG files from assemblies")
        out_dir = "./body-thumbnails"

    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.mkdir(out_dir)

    for assembly in tqdm(assemblies, desc="Processing assemblies"):
        if args.feature == "assembly_json":
            for json_file in glob.iglob(os.path.join(args.input + '\\' + assembly, "*.json")):
                source = json_file
                dest = out_dir + '\\' + f"{assembly}.json"
                shutil.copy(source, dest)
        elif args.feature == "assembly_thumbnail":
            for jpg_file in glob.iglob(os.path.join(args.input + '\\' + assembly, "*.jpg")):
                name = jpg_file.split("\\")[-1].split('.jpg')[0]
                if name == "assembly":
                    source = jpg_file
                    dest = out_dir + '\\' + f"{assembly}.jpg"
                    shutil.copy(source, dest)
        else:
            for jpg_file in glob.iglob(os.path.join(args.input + '\\' + assembly, "*.jpg")):
                name = jpg_file.split("\\")[-1].split('.jpg')[0]
                if name != "assembly":
                    source = jpg_file
                    name = f"{assembly}_sep_{name}"
                    dest = out_dir + '\\' + f"{name}.jpg"
                    shutil.copy(source, dest)


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--feature', type=str)
    parser.add_argument('--input', type=str, default="../../dataset")
    return parser.parse_args()


if __name__ == "__main__":
    args = get_parser()

    if args.feature not in ["assembly_json", "assembly_thumbnail", "body_thumbnail"]:
        print("ERROR: invalid feature choice!")
        exit(1)

    extraction(args)
