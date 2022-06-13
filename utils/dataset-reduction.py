"""
Reduce the size of the assembly dataset by reducing the size of the PNG image files
"""
import os
import shutil
import glob
from tqdm import tqdm
import json
import cv2
from PIL import Image, ImageDraw, ImageFont


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


if __name__ == "__main__":
    image_size_reduction("filtered_dataset")
